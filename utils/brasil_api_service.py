import requests


class BrasilAPIService:
    BASE_URL = "https://brasilapi.com.br/api"

    def get_ncm(self, ncm):
        url = f"{self.BASE_URL}/ncm/v1/{ncm}"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()

        return None
