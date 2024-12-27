import uuid
from http import HTTPStatus

from django.http import JsonResponse
from ninja.errors import HttpError

from apps.taxes.models import Tax
from apps.taxes.schema import TaxCreateSchema, TaxUpdateSchema
from utils.validation import ValidationService


class TaxesService:
    MAX_ENTRIES = 10

    def __init__(self):
        self.validation_service = ValidationService()

    @staticmethod
    def get_tax_by_id(tax_id: uuid.UUID):
        return Tax.objects.filter(pk=tax_id).first()

    @staticmethod
    def list_taxes():
        taxes = Tax.objects.all()
        count = taxes.count()

        return {
            "count": count,
            "total_presumed_profit_rate": Tax.total_presumed_profit_rate(),
            "total_real_profit_rate": Tax.total_real_profit_rate(),
            "taxes": taxes,
        }

    def get_tax(self, tax_id: uuid.UUID):
        if not (tax := self.get_tax_by_id(tax_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Imposto não encontrado")

        return tax

    def create_tax(self, jwt: dict, payload: TaxCreateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Usuário não autorizado")

        if Tax.objects.count() >= self.MAX_ENTRIES:
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                f"O limite de {self.MAX_ENTRIES} impostos foi atingido.",
            )

        return Tax.objects.create(**payload.dict())

    def update_tax(self, jwt: dict, tax_id: uuid.UUID, payload: TaxUpdateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Usuário não autorizado")

        tax = self.get_tax(tax_id)

        for attr, value in payload.model_dump(
            exclude_defaults=True, exclude_unset=True
        ).items():
            setattr(tax, attr, value)

        tax.save()
        return tax

    def delete_tax(self, jwt: dict, tax_id: uuid.UUID):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Usuário não autorizado")

        tax = self.get_tax(tax_id)
        tax.delete()
        
        return JsonResponse(
            {"detail": "Imposto deletado com sucesso"}, status=HTTPStatus.OK
        )
