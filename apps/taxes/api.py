import uuid

from ninja import Router

from apps.taxes.schema import TaxCreateSchema, TaxListSchema, TaxSchema, TaxUpdateSchema
from apps.taxes.service import TaxesService

taxes_router = Router()
service = TaxesService()


@taxes_router.post("", response=TaxSchema)
def create_tax(request, payload: TaxCreateSchema):
    return service.create_tax(payload)


@taxes_router.get("", response=TaxListSchema)
def list_taxes(request):
    return service.list_taxes()


@taxes_router.get("/{tax_id}", response=TaxSchema)
def get_tax(request, tax_id: uuid.UUID):
    return service.get_tax(tax_id)


@taxes_router.patch("/{tax_id}", response=TaxSchema)
def update_tax(request, tax_id: uuid.UUID, payload: TaxUpdateSchema):
    return service.update_tax(tax_id, payload)


@taxes_router.delete("/{tax_id}")
def delete_tax(request, tax_id: uuid.UUID):
    return service.delete_tax(tax_id)
