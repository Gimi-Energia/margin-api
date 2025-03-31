import requests
from django.conf import settings


class ErrorNotificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            if response.status_code == 500:
                self.process_exception(request, exception=response)
            return response
        except Exception as exception:
            self.process_exception(request, exception)
            return

    def process_exception(self, request, exception):
        # if settings.DEBUG:
        #     return None

        exception_message = exception.reason_phrase
        exception_detail = exception.content.decode("utf-8")

        error_message = {
            "cards": [
                {
                    "header": {
                        "title": "⚠️ Erro 500 Detectado",
                        "subtitle": str(exception_message),
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": f"💻 <b>API</b>: Margin<br>"
                                        f"📍 <b>Path</b>: {request.path}<br>"
                                        f"🔧 <b>Method</b>: {request.method}<br><br>"
                                        f"📝 <b>Traceback</b>:<br>{exception_detail}"
                                    }
                                }
                            ]
                        }
                    ],
                }
            ]
        }

        if not (webhook_url := getattr(settings, "GOOGLE_CHAT_WEBHOOK_URL")):
            print("⚠️ Webhook do Google Chat não configurado no settings.")
            return None

        try:
            requests.post(
                webhook_url,
                json=error_message,
                headers={"Content-Type": "application/json"},
                timeout=5,
            )
        except requests.RequestException as e:
            print(f"⚠️ Falha ao enviar erro para o Google Chat: {e}")

        return None
