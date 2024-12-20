import uuid

from ninja import Router

from apps.taxes.schema import TaxCreateSchema, TaxListSchema, TaxSchema, TaxUpdateSchema
from apps.taxes.service import TaxesService
from utils.jwt import JWTAuth, decode_jwt_token

taxes_router = Router(auth=JWTAuth())
service = TaxesService()


@taxes_router.post("", response=TaxSchema)
def create_tax(request, payload: TaxCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return service.create_tax(jwt, payload)


@taxes_router.get("", response=TaxListSchema)
def list_taxes(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list_taxes()


@taxes_router.get("/{tax_id}", response=TaxSchema)
def get_tax(request, tax_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.get_tax(tax_id)


@taxes_router.patch("/{tax_id}", response=TaxSchema)
def update_tax(request, tax_id: uuid.UUID, payload: TaxUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return service.update_tax(jwt, tax_id, payload)


@taxes_router.delete("/{tax_id}")
def delete_tax(request, tax_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return service.delete_tax(jwt, tax_id)
