import uuid
from http import HTTPStatus
from django.db import IntegrityError
from django.http import JsonResponse
from ninja.errors import HttpError

from apps.margin.models import Company
from apps.margin.schema import CompanyCreateSchema, CompanyUpdateSchema
from utils.validation import ValidationService


class CompanyService:
    def __init__(self):
        self.validation_service = ValidationService()

    @staticmethod
    def get_company_by_id(company_id: uuid.UUID):
        return Company.objects.filter(pk=company_id).first()

    @staticmethod
    def list_companies():
        companies = Company.objects.all()
        count = companies.count()

        return {
            "count": count,
            "companies": companies,
        }

    def get_company(self, company_id: uuid.UUID):
        if not (company := self.get_company_by_id(company_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Empresa não encontrada")

        return company

    def create_company(self, jwt: dict, payload: CompanyCreateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Usuário não autorizado")

        try:
            return Company.objects.create(**payload.dict())
        except IntegrityError as exc:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Empresa já existe") from exc

    def update_company(
        self, jwt: dict, company_id: uuid.UUID, payload: CompanyUpdateSchema
    ):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Usuário não autorizado")

        company = self.get_company(company_id)

        for attr, value in payload.model_dump(
            exclude_defaults=True, exclude_unset=True
        ).items():
            setattr(company, attr, value)

        try:
            company.save()
        except IntegrityError as exc:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Empresa já existe") from exc

        return company

    def delete_company(self, jwt: dict, company_id: uuid.UUID):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Usuário não autorizado")

        company = self.get_company(company_id)
        company.delete()

        return JsonResponse(
            {"detail": "Empresa deletada com sucesso"}, status=HTTPStatus.OK
        )
