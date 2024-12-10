import uuid

from ninja import Router

from .schema import TaxCreateSchema, TaxListSchema, TaxSchema, TaxUpdateSchema
from .service import TaxesService

taxes_router = Router()
service = TaxesService()


@taxes_router.get("/taxes", response=TaxListSchema)
def list_taxes(request):
    return service.list_taxes()


@taxes_router.get("/taxes/{tax_id}", response=TaxSchema)
def get_tax(request, tax_id: uuid.UUID):
    return service.get_tax(tax_id)


@taxes_router.post("/taxes", response=TaxSchema)
def create_tax(request, payload: TaxCreateSchema):
    return service.create_tax(payload)


@taxes_router.patch("/taxes/{tax_id}", response=TaxSchema)
def update_tax(request, tax_id: uuid.UUID, payload: TaxUpdateSchema):
    return service.update_tax(tax_id, payload)
