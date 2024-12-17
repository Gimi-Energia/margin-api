import os
import uuid
from http import HTTPStatus

import requests
from ninja.errors import HttpError

from apps.icms.services.icms_service import ICMSService
from apps.icms.services.ncm_service import NCMService
from apps.icms.services.state_service import StateService
from apps.margin.services.company_service import CompanyService
from apps.taxes.models import Tax


class ContractService:
    @property
    def ncm_service(self):
        return NCMService()

    @property
    def state_service(self):
        return StateService()

    @property
    def company_service(self):
        return CompanyService()

    @property
    def icms_service(self):
        return ICMSService()

    def find_iapp_contract(self, company_id: uuid.UUID, contract: str):
        if not (company := self.company_service.get_company_by_id(company_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Empresa não encontrada")

        token, secret = self._get_credentials(company)
        items = self._fetch_contract_data(contract, token, secret)

        item = items[0]
        products = self.validate_field(item.get("produtos"), "produtos")
        ncm_obj = self._validate_ncm(products)

        other_taxes = self._calculate_other_taxes(company.profit_type)

        state = self.validate_field(item.get("cliente").get("estado"), "cliente.estado")
        if not (state_obj := self.state_service.get_state_by_code(state)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

        if not (
            icms_obj := self.icms_service.get_rate_by_state_and_ncm(state, ncm_obj.code)
        ):
            raise HttpError(HTTPStatus.NOT_FOUND, "Taxa de ICMS não encontrada")

        net_cost, net_cost_without_taxes = self._calculate_net_costs(
            item, icms_obj.total_rate, other_taxes
        )

        contract_data = {
            "contract_id": self.validate_field(item.get("id"), "id"),
            "contract_number": self.validate_field(
                item.get("identificacao"), "identificacao"
            ),
            "company": company,
            "client_name": self.validate_field(
                item.get("cliente").get("nome"), "cliente.nome"
            ),
            "client_id": self.validate_field(
                item.get("cliente").get("id"), "cliente.id"
            ),
            "construction_name": self.validate_field(
                item.get("projeto").get("nome"), "projeto.nome"
            ),
            "delivery_date": self.validate_field(
                item.get("datas").get("previsao_entrega"), "datas.previsao_entrega"
            ),
            "net_cost": net_cost,
            "net_cost_without_taxes": net_cost_without_taxes,
            "net_cost_with_margin": None,
            "freight_value": item.get("valores").get("valor_frete", 0),
            "commission": float(
                item.get("vendedor")
                .get("nome", "Gimi_0%")
                .split("_")[1][:-1]
                .replace(",", ".")
            ),
            "state": state_obj,
            "ncm": ncm_obj,
            "icms": icms_obj,
            "other_taxes": other_taxes,
            "account": self.validate_field(
                item.get("conta_corrente"), "conta_corrente"
            ),
            "installments": self.validate_field(
                item.get("parcelamento"), "parcelamento"
            ),
            "xped": item.get("xped", "N/A"),
            "margin": None,
            "items": [
                {
                    "index": index,
                    "sale_item_id": product["id"],
                    "quantity": product["qtde"],
                    "product_id": product["produto"].get("id"),
                    "name": self.validate_field(
                        product["produto"].get("identificacao"),
                        f"produto.{index}.identificacao",
                    ),
                    "contribution_rate": (
                        (
                            self.validate_field(
                                product["valores"].get("unitario"),
                                f"valores.{index}.unitario",
                            )
                            / item["valores"]["valor_produtos"]
                        )
                        * 100
                    )
                    if item["valores"]["valor_produtos"] > 0
                    else 0,
                    "updated_value": None,
                }
                for index, product in enumerate(products, start=1)
            ],
        }
        return contract_data

    def _get_credentials(self, company):
        token = str(os.getenv(f"TOKEN_{company.name}"))
        secret = str(os.getenv(f"SECRET_{company.name}"))
        if not token or not secret:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Credenciais não configuradas.")
        return token, secret

    def _fetch_contract_data(self, contract, token, secret):
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

            if items := iapp_response.get("response"):
                return items
            raise HttpError(HTTPStatus.NOT_FOUND, "Contrato não encontrado.")

        raise HttpError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            f"Erro {response.status_code}: Instabilidade no iApp.",
        )

    def _validate_ncm(self, products):
        ncm_values = {product.get("produto").get("ncm") for product in products}

        if len(ncm_values) > 1:
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                "Todos os produtos devem ter o mesmo NCM.",
            )

        ncm = next(iter(ncm_values))
        if not (ncm_obj := self.ncm_service.get_ncm_by_code(ncm)):
            raise HttpError(HTTPStatus.NOT_FOUND, "NCM não encontrado")

        return ncm_obj

    def _calculate_other_taxes(self, company_type):
        return (
            Tax.total_real_profit_rate()
            if company_type == "real"
            else Tax.total_presumed_profit_rate()
        )

    def _calculate_net_costs(self, item, icms_rate, other_taxes):
        net_cost = self.validate_field(
            item.get("valores").get("valor_produtos"), "valor_produtos"
        )
        icms_rate = float(icms_rate) / 100
        other_taxes_rate = float(other_taxes) / 100
        total_taxes = 1 + (icms_rate + other_taxes_rate)
        net_cost_without_taxes = net_cost / total_taxes
        return net_cost, net_cost_without_taxes

    def raise_error(self, field):
        raise HttpError(
            HTTPStatus.BAD_REQUEST, f"Campo obrigatório ausente no iApp: '{field}'."
        )

    def validate_field(self, field, field_name):
        if field is None:
            self.raise_error(field_name)
        return field
