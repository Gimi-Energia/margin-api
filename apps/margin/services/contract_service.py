import os
import uuid
from http import HTTPStatus

import requests
from ninja.errors import HttpError

from apps.icms.services.icms_service import ICMSService
from apps.margin.services.company_service import CompanyService
from apps.taxes.models import Tax


class ContractService:
    @property
    def company_service(self):
        return CompanyService()

    @property
    def icms_service(self):
        return ICMSService()

    def find_iapp_contract(self, company_id: uuid.UUID, contract: str):
        if not (company := self.company_service.get_company_by_id(company_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Empresa não encontrada")

        token = str(os.getenv(f"TOKEN_{company.name}"))
        secret = str(os.getenv(f"SECRET_{company.name}"))

        if not token or not secret:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Credenciais não configuradas.")

        ENDPOINT = (
            "https://api.iniciativaaplicativos.com.br/api/comercial/contratos/lista"
        )
        headers = {"TOKEN": token, "SECRET": secret}

        params = {"offset": 1, "page": 1, "filters": f"identificacao|{contract}"}

        response = requests.get(ENDPOINT, params=params, headers=headers)

        if response.ok:
            iapp_response = response.json()

            if iapp_response.get("success") is False:
                raise HttpError(HTTPStatus.BAD_REQUEST, iapp_response.get("message"))

            if items := iapp_response.get("response", []):
                item = items[0]

                products = item.get("produtos", [])

                ncm_values = {
                    product.get("produto", {}).get("ncm", "N/A") for product in products
                }

                if len(ncm_values) > 1:
                    raise HttpError(
                        HTTPStatus.BAD_REQUEST,
                        "Todos os produtos devem ter o mesmo NCM.",
                    )

                ncm = next(iter(ncm_values))

                company_type = company.profit_type
                other_taxes = 0
                if company_type == "real":
                    other_taxes = Tax.total_real_profit_rate()
                elif company_type == "presumed":
                    other_taxes = Tax.total_presumed_profit_rate()

                state = item.get("cliente", {}).get("estado", "N/A")
                ncm = item.get("produtos", [])[0].get("produto", {}).get("ncm", "N/A")

                if not (
                    icms := self.icms_service.get_rate_by_state_and_ncm(state, ncm)
                ):
                    raise HttpError(HTTPStatus.NOT_FOUND, "Taxa de ICMS não encontrada")

                contract_data = {
                    "contract_id": item.get("id", "N/A"),
                    "contract_number": item.get("identificacao", "N/A"),
                    "company": item.get("codigo_empresa", "N/A"),
                    "client_name": item.get("cliente", {}).get("nome", "N/A"),
                    "client_id": item.get("cliente").get("id", "N/A"),
                    "construction_name": item.get("projeto", {}).get("nome", "N/A"),
                    "current_sale_value": item.get("valores", {}).get("valor_total", 0),
                    "cost_value": item.get("valores", {}).get("valor_produtos", 0),
                    "freight_value": item.get("valores", {}).get("valor_frete", 0),
                    "commission": float(
                        item.get("vendedor", {})
                        .get("nome", "Gimi_0%")
                        .split("_")[1][:-1]
                        .replace(",", ".")
                    ),
                    "account": item.get("conta_corrente", "N/A"),
                    "installments": item.get("parcelamento", "N/A"),
                    "xped": item.get("xped", "N/A"),
                    "state": state,
                    "icms": icms.total_rate,
                    "other_taxes": other_taxes,
                    "items": [
                        {
                            "index": index,
                            "name": product.get("produto", {}).get(
                                "identificacao", "N/A"
                            ),
                            "ncm": product.get("produto", {}).get("ncm", "N/A"),
                            "current_value": product.get("valores", {}).get(
                                "unitario", 0
                            ),
                            "contribution_percentage": (
                                (
                                    product.get("valores", {}).get("unitario", 0)
                                    / item.get("valores", {}).get("valor_produtos", 1)
                                )
                                * 100
                            )
                            if item.get("valores", {}).get("valor_produtos", 0) > 0
                            else 0,
                        }
                        for index, product in enumerate(products, start=1)
                    ],
                }
                return contract_data

            raise HttpError(HTTPStatus.NOT_FOUND, "Contrato não encontrado.")

        raise HttpError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            f"Erro {response.status_code}: Instabilidade no iApp.",
        )
