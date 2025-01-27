from http import HTTPStatus

from babel.numbers import format_currency, format_percent
from django.conf import settings
from django.core.mail import send_mail
from ninja.errors import HttpError

from apps.margin.models import Contract


class EmailService:
    @staticmethod
    def send_margin_email(contract: Contract):
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [
            "dev2@engenhadev.com",
            "bruno@engenhadev.com",
            "dev3@engenhadev.com",
        ]
        email_subject = f"App Margem - Retorno do Contrato {contract.contract_number} ({contract.company})"
        email_body = f"""
        <html>
        <head>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                }}
                h3, h2 {{
                    color: #333;
                }}
                ul {{
                    list-style-type: none;
                    padding: 0;
                }}
                ul li {{
                    margin-bottom: 10px;
                }}
                table {{
                    width: 100%;
                    border-collapse: collapse;
                    margin-top: 20px;
                }}
                table, th, td {{
                    border: 1px solid #ddd;
                }}
                th, td {{
                    padding: 8px;
                    text-align: left;
                }}
                th {{
                    background-color: #f2f2f2;
                }}
                .button {{
                    display: inline-block;
                    background-color: #f0f0f0;
                    padding: 8px 16px;
                    text-align: center;
                    text-decoration: none;
                    font-size: 16px;
                    border-radius: 10px;
                    margin-top: 10px;
                    border: 2px solid black;
                    font-weight: bold;
                    transition: background-color 0.2s ease;
                }}
                .button:hover {{
                    background-color: #e0e0e0;
                }}
            </style>
        </head>
        <body>
            <h2>🎉 Contrato retornado com sucesso.</h2>
            <h3>Detalhes do contrato:</h3>
            <ul>
                <li><strong>Número:</strong> {contract.contract_number}</li>
                <li><strong>Empresa:</strong> {contract.company}</li>
                <li><strong>Cliente:</strong> {contract.client_name}</li>
                <li><strong>Obra:</strong> {contract.construction_name}</li>
                <li><strong>Estado:</strong> {contract.state.name}</li>
                <li><strong>NCM:</strong> {contract.ncm.code}</li>
                <li><strong>Frete:</strong> {format_currency(contract.freight_value, "BRL", locale="pt_BR")}</li>
                <li><strong>Comissão:</strong> {format_percent(contract.commission / 100, format="0.00%", locale="pt_BR")}</li>
                <li><strong>ICMS:</strong> {format_percent(contract.icms.total_rate / 100, format="0.00%", locale="pt_BR")}</li>
                <li><strong>Outros impostos:</strong> {format_percent(contract.other_taxes / 100, format="0.00%", locale="pt_BR")}</li>
                <li><strong>Margem:</strong> {format_percent(contract.margin.value / 100, format="0.00%", locale="pt_BR")}</li>
                <li><strong>Total:</strong> {format_currency(contract.net_cost, "BRL", locale="pt_BR")}</li>
                <li><strong>Total sem impostos:</strong> {format_currency(contract.net_cost_without_taxes, "BRL", locale="pt_BR")}</li>
                <li><strong>Total com margem:</strong> {format_currency(contract.net_cost_with_margin, "BRL", locale="pt_BR")}</li>
            </ul>
            <a href="https://iapp.iniciativaaplicativos.com.br/comercial/contratos/editar?id={contract.contract_id}" class="button">Ver Contrato</a>
            <h3>Itens do contrato:</h3>
            <table>
                <thead>
                    <tr>
                        <th>Item</th>
                        <th>Nome</th>
                        <th>Contribuição</th>
                        <th>Valor Unitário</th>
                    </tr>
                </thead>
                <tbody>
        """

        for item in contract.items.all():
            email_body += f"""
                    <tr>
                        <td>{item.index}</td>
                        <td>{item.name}</td>
                        <td>{format_percent(item.contribution_rate / 100, format="0.00%", locale="pt_BR")}</td>
                        <td>{format_currency(item.updated_value, "BRL", locale="pt_BR")}</td>
                    </tr>
            """

        email_body += """
                </tbody>
            </table>
        </body>
        </html>
        """

        try:
            send_mail(
                subject=email_subject,
                message=email_subject,
                from_email=email_from,
                recipient_list=recipient_list,
                html_message=email_body,
                fail_silently=False,
            )
        except Exception as e:
            raise HttpError(
                HTTPStatus.INTERNAL_SERVER_ERROR, f"Erro ao enviar e-mail: {str(e)}"
            ) from e
