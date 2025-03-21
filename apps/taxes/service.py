import uuid
from http import HTTPStatus

from django.db import IntegrityError
from django.http import JsonResponse
from ninja.errors import HttpError

from apps.margin.services.company_service import CompanyService
from apps.taxes.models import Tax
from apps.taxes.schema import TaxCreateSchema, TaxUpdateSchema
from utils.validation import ValidationService


class TaxesService:
    MAX_ENTRIES = 10

    def __init__(self):
        self.validation_service = ValidationService()
        self.company_service = CompanyService()

    @staticmethod
    def get_tax_by_id(tax_id: uuid.UUID):
        return Tax.objects.filter(pk=tax_id).first()

    @staticmethod
    def count_taxes() -> int:
        return Tax.objects.count()

    @staticmethod
    def list_taxes():
        taxes = Tax.objects.all()
        count = taxes.count()

        return {
            "count": count,
            "total_presumed_profit_rate": Tax.total_presumed_profit_rate(),
            "total_presumed_profit_rate_with_deduct": Tax.total_presumed_profit_rate_with_deduct(),
            "total_real_profit_rate": Tax.total_real_profit_rate(),
            "total_real_profit_rate_with_deduct": Tax.total_real_profit_rate_with_deduct(),
            "taxes": taxes,
        }

    def get_tax(self, tax_id: uuid.UUID):
        if not (tax := self.get_tax_by_id(tax_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Imposto não encontrado")

        return tax

    def create_tax(self, jwt: dict, payload: TaxCreateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        if Tax.objects.count() >= self.MAX_ENTRIES:
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                f"O limite de {self.MAX_ENTRIES} impostos foi atingido.",
            )

        try:
            return Tax.objects.create(**payload.dict())
        except IntegrityError as exc:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Esse imposto já existe") from exc
        except Exception as exc:
            raise HttpError(
                HTTPStatus.INTERNAL_SERVER_ERROR, "Erro ao criar imposto"
            ) from exc

    def update_tax(self, jwt: dict, tax_id: uuid.UUID, payload: TaxUpdateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        tax = self.get_tax(tax_id)

        for attr, value in payload.model_dump(
            exclude_defaults=True, exclude_unset=True
        ).items():
            setattr(tax, attr, value)

        try:
            tax.save()
        except IntegrityError as exc:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Esse imposto já existe") from exc
        except Exception as exc:
            raise HttpError(
                HTTPStatus.INTERNAL_SERVER_ERROR, "Erro ao atualizar imposto"
            ) from exc

        return tax

    def delete_tax(self, jwt: dict, tax_id: uuid.UUID):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        if self.count_taxes() <= 1:
            raise HttpError(
                HTTPStatus.BAD_REQUEST, "Não é possível deletar o último imposto"
            )

        tax = self.get_tax(tax_id)
        tax.delete()

        return JsonResponse(
            {"detail": "Imposto deletado com sucesso"}, status=HTTPStatus.OK
        )

    def list_taxes_by_company(self, company_id: uuid.UUID):
        company = self.company_service.get_company(company_id)
        taxes = Tax.list_taxes_by_company(company)
        return list(taxes)
