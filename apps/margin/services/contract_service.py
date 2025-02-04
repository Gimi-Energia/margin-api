import os
import uuid
from datetime import datetime
from http import HTTPStatus

import requests
from django.db import transaction
from ninja.errors import HttpError

from apps.icms.services.icms_service import ICMSService
from apps.icms.services.ncm_service import NCMService
from apps.icms.services.state_service import StateService
from apps.margin.models import Contract, ContractItem
from apps.margin.services.company_service import CompanyService
from apps.margin.services.email_service import EmailService
from apps.margin.services.percentage_service import PercentageService
from apps.taxes.models import Tax
from utils.gimix_service import GIMIxService


class ContractService:
    def __init__(self):
        self.ncm_service = NCMService()
        self.state_service = StateService()
        self.company_service = CompanyService()
        self.icms_service = ICMSService()
        self.percentage_service = PercentageService()
        self.email_service = EmailService()
        self.gimix_service = GIMIxService()

    @staticmethod
    def get_contract_by_id(contract_id: uuid.UUID):
        return Contract.objects.filter(pk=contract_id).first()

    def return_iapp_contract(self, contract_id: uuid.UUID, user_email: str, token: str):
        if not (contract := self.get_contract_by_id(contract_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Contrato não encontrado")

        token, secret = self._get_credentials(contract.company)
        payload = self._prepare_update_payload(contract)
        self._update_contract_data(contract.contract_id, payload, token, secret)

        recipients = self.gimix_service.get_margin_admins_email(token)
        recipients.append(user_email)

        self.email_service.send_margin_email(contract, recipients)

        return {
            "detail": f"Retorno do contrato {contract.contract_number} realizado com sucesso.",
            "url": f"https://iapp.iniciativaaplicativos.com.br/comercial/contratos/editar?id={contract.contract_id}",
        }

    def _prepare_update_payload(self, contract: Contract):
        items = [
            {
                "produto": item.product_id,
                "qtde": item.quantity,
                "valor_unitario": item.updated_value,
                "id": item.sale_item_id,
            }
            for item in contract.items.all()
        ]

        response = {
            "cliente": contract.client_id,
            "numero_controle": contract.contract_number,
            "data_entrega": contract.delivery_date.strftime("%Y-%m-%d"),
            "xped": contract.xped,
            "conta_corrente": contract.account,
            "parcelamento": contract.installments,
            "produtos": items,
        }

        return response

    def _update_contract_data(self, contract_id, payload, token, secret):
        ENDPOINT = f"https://api.iniciativaaplicativos.com.br/api/comercial/contratos/atualiza/{contract_id}"
        headers = {"TOKEN": token, "SECRET": secret}

        response = requests.put(ENDPOINT, json=payload, headers=headers, timeout=10)

        if response.ok:
            iapp_response = response.json()

            if iapp_response.get("success") is False:
                raise HttpError(HTTPStatus.BAD_REQUEST, iapp_response.get("message"))

            return

        raise HttpError(
            HTTPStatus.INTERNAL_SERVER_ERROR,
            f"Erro {response.status_code}: Instabilidade no iApp.",
        )

    def calculate_iapp_contract(self, contract_id: uuid.UUID, percentage_id: uuid.UUID):
        if not (contract := self.get_contract_by_id(contract_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Contrato não encontrada")

        percentage = self.percentage_service.get_percentage(percentage_id)
        margin = percentage.value

        sale_price = (
            float(contract.net_cost_without_taxes) + float(contract.freight_value)
        ) / (
            1
            - (float(contract.icms.total_rate) / 100)
            - (float(contract.other_taxes) / 100)
            - (float(margin) / 100)
            - (float(contract.commission) / 100)
        )

        sale_price = round(sale_price + 0.5)

        with transaction.atomic():
            contract.net_cost_with_margin = sale_price
            contract.margin = percentage
            contract.save()

            items = contract.items.all()
            for item in items:
                item.updated_value = (sale_price * item.contribution_rate) / 100
                item.save()

        return self._prepare_calculated_response(contract)

    def _prepare_calculated_response(self, contract: Contract):
        items_data = [
            {
                "id": item.id,
                "index": item.index,
                "name": item.name,
                "contribution_rate": item.contribution_rate,
                "updated_value": item.updated_value,
            }
            for item in contract.items.all()
        ]

        return {
            "id": contract.id,
            "contract_number": contract.contract_number,
            "company": contract.company,
            "client_name": contract.client_name,
            "construction_name": contract.construction_name,
            "net_cost": contract.net_cost,
            "net_cost_without_taxes": contract.net_cost_without_taxes,
            "freight_value": contract.freight_value,
            "commission": contract.commission,
            "state": contract.state,
            "ncm": contract.ncm,
            "icms": contract.icms,
            "other_taxes": contract.other_taxes,
            "items": items_data,
            "net_cost_with_margin": contract.net_cost_with_margin,
            "margin": contract.margin,
        }

    def find_iapp_contract(self, company_id: uuid.UUID, contract: str):
        company = self.company_service.get_company(company_id)

        token, secret = self._get_credentials(company)
        items = self._get_contract_data(contract, token, secret)

        item = items[0]
        products = self.validate_field(item.get("produtos"), "produtos")

        if len(products) == 0:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Contrato sem produtos.")

        ncm_instance = self._validate_ncm(products)

        other_taxes = self._calculate_other_taxes(company.profit_type)

        state = self.validate_field(item.get("cliente").get("estado"), "cliente.estado")
        if not (state_instance := self.state_service.get_state_by_code(state)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

        if not (
            icms_instance := self.icms_service.get_rate_by_state_and_ncm(
                state, ncm_instance.code
            )
        ):
            raise HttpError(HTTPStatus.NOT_FOUND, "Taxa de ICMS não encontrada")

        net_cost, net_cost_without_taxes = self._calculate_net_costs(item, other_taxes)

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
            "delivery_date": datetime.strptime(
                self.validate_field(
                    item.get("datas").get("data_previsao_faturamento"),
                    "datas.data_previsao_faturamento",
                ),
                "%Y-%m-%d",
            ).date(),
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
            "state": state_instance,
            "ncm": ncm_instance,
            "icms": icms_instance,
            "other_taxes": other_taxes,
            "account": self.validate_field(
                item.get("conta_corrente"), "conta_corrente"
            ),
            "installments": self.validate_field(
                item.get("parcelamento"), "parcelamento"
            ),
            "xped": item.get("xped") or "N/A",
            "margin": None,
            "items": [
                {
                    "index": index,
                    "sale_item_id": product["id"],
                    "quantity": product["qtde"],
                    "product_id": product["produto"].get("id"),
                    "name": self.validate_field(
                        product["tags"].get("produto"), f"tags.{index}.produto"
                    ),
                    "contribution_rate": (
                        (
                            self.validate_field(
                                product["valores"].get("valor_produtos_sem_icms"),
                                f"valores.{index}.valor_produtos_sem_icms",
                            )
                            / item["valores"]["valor_produtos_sem_icms"]
                        )
                        * 100
                    )
                    if item["valores"]["valor_produtos_sem_icms"] > 0
                    else 0,
                    "updated_value": None,
                }
                for index, product in enumerate(products, start=1)
            ],
        }

        contract_data_with_ids = self._save_contract(contract_data)
        return contract_data_with_ids

    def _get_credentials(self, company):
        token = str(os.getenv(f"TOKEN_{company.name}"))
        secret = str(os.getenv(f"SECRET_{company.name}"))
        if not token or not secret:
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Credenciais não configuradas.")
        return token, secret

    def _get_contract_data(self, contract, token, secret):
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
        if not (ncm_instance := self.ncm_service.get_ncm_by_code(ncm)):
            raise HttpError(HTTPStatus.NOT_FOUND, "NCM não encontrado")

        return ncm_instance

    def _calculate_other_taxes(self, company_type):
        return (
            Tax.total_real_profit_rate()
            if company_type == "real"
            else Tax.total_presumed_profit_rate()
        )

    def _calculate_net_costs(self, item, other_taxes):
        products = item.get("produtos")
        net_cost = sum(
            self.validate_field(
                product.get("valores").get("valor_produtos_sem_icms"),
                "valores.valor_produtos_sem_icms",
            )
            for product in products
        )
        other_taxes_rate = float(other_taxes) / 100
        total_taxes = 1 + other_taxes_rate
        net_cost_without_taxes = net_cost / total_taxes
        return net_cost, net_cost_without_taxes

    def _save_contract(self, contract_data):
        try:
            with transaction.atomic():
                contract = Contract.objects.create(
                    contract_id=contract_data["contract_id"],
                    contract_number=contract_data["contract_number"],
                    company=contract_data["company"],
                    client_name=contract_data["client_name"],
                    client_id=contract_data["client_id"],
                    construction_name=contract_data["construction_name"],
                    delivery_date=contract_data["delivery_date"],
                    net_cost=contract_data["net_cost"],
                    net_cost_without_taxes=contract_data["net_cost_without_taxes"],
                    net_cost_with_margin=contract_data["net_cost_with_margin"],
                    freight_value=contract_data["freight_value"],
                    commission=contract_data["commission"],
                    state=contract_data["state"],
                    ncm=contract_data["ncm"],
                    icms=contract_data["icms"],
                    other_taxes=contract_data["other_taxes"],
                    account=contract_data["account"],
                    installments=contract_data["installments"],
                    xped=contract_data["xped"],
                    margin=contract_data["margin"],
                )
                contract_data["id"] = contract.id

                for index, item in enumerate(contract_data["items"]):
                    item_instance = ContractItem.objects.create(
                        contract=contract,
                        index=item["index"],
                        name=item["name"],
                        contribution_rate=item["contribution_rate"],
                        sale_item_id=item["sale_item_id"],
                        quantity=item["quantity"],
                        product_id=item["product_id"],
                        updated_value=item["updated_value"],
                    )
                    contract_data["items"][index]["id"] = item_instance.id

            return contract_data
        except Exception as e:
            raise HttpError(
                HTTPStatus.INTERNAL_SERVER_ERROR, f"Erro ao salvar contrato: {e}."
            ) from e

    def raise_error(self, field):
        raise HttpError(
            HTTPStatus.BAD_REQUEST, f"Campo obrigatório ausente no iApp: '{field}'."
        )

    def validate_field(self, field, field_name):
        if field is None:
            self.raise_error(field_name)
        return field
