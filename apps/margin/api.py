import uuid

from ninja import Router

from apps.margin.schema import (
    CompanyCreateSchema,
    CompanyListSchema,
    CompanySchema,
    CompanyUpdateSchema,
    PercentageListSchema,
    PercentageSchema,
    PercentageUpdateSchema,
)
from apps.margin.services.company_service import CompanyService
from apps.margin.services.percentages_service import PercentageService

company_router = Router()
company_service = CompanyService()

percentage_router = Router()
percentage_service = PercentageService()


@company_router.post("", response=CompanySchema)
def create_company(request, payload: CompanyCreateSchema):
    return company_service.create_company(payload)


@company_router.get("", response=CompanyListSchema)
def list_companies(request):
    return company_service.list_companies()


@company_router.get("/{company_id}", response=CompanySchema)
def get_company(request, company_id: uuid.UUID):
    return company_service.get_company(company_id)


@company_router.patch("/{company_id}", response=CompanySchema)
def update_company(request, company_id: uuid.UUID, payload: CompanyUpdateSchema):
    return company_service.update_company(company_id, payload)


@company_router.delete("/{company_id}")
def delete_company(request, company_id: uuid.UUID):
    return company_service.delete_company(company_id)


@percentage_router.get("", response=PercentageListSchema)
def list_percentages(request):
    return percentage_service.list_percentages()


@percentage_router.get("/{percentage_id}", response=PercentageSchema)
def get_percentage(request, percentage_id: uuid.UUID):
    return percentage_service.get_percentage(percentage_id)


@percentage_router.patch("/{percentage_id}", response=PercentageSchema)
def update_percentage(
    request, percentage_id: uuid.UUID, payload: PercentageUpdateSchema
):
    return percentage_service.update_percentage(percentage_id, payload)
