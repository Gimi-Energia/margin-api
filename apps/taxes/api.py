import uuid
from http import HTTPStatus

from ninja import Router

from apps.taxes.schema import (
    TaxByCompanySchema,
    TaxCreateSchema,
    TaxListSchema,
    TaxSchema,
    TaxUpdateSchema,
)
from apps.taxes.service import TaxesService
from utils.base_schema import ErrorSchema
from utils.jwt import JWTAuth, decode_jwt_token

taxes_router = Router(auth=JWTAuth())
service = TaxesService()


@taxes_router.post(
    "",
    response={
        HTTPStatus.CREATED: TaxSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_tax(request, payload: TaxCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return service.create_tax(jwt, payload)


@taxes_router.get(
    "", response={HTTPStatus.OK: TaxListSchema, HTTPStatus.FORBIDDEN: ErrorSchema}
)
def list_taxes(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list_taxes()


@taxes_router.get(
    "/{tax_id}",
    response={
        HTTPStatus.OK: TaxSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def get_tax(request, tax_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.get_tax(tax_id)


@taxes_router.get(
    "/by-company/{company_id}",
    response={
        HTTPStatus.OK: list[TaxByCompanySchema],
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def list_taxes_by_company(request, company_id: uuid.UUID):
    return service.list_taxes_by_company(company_id)


@taxes_router.patch(
    "/{tax_id}",
    response={
        HTTPStatus.OK: TaxSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def update_tax(request, tax_id: uuid.UUID, payload: TaxUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return service.update_tax(jwt, tax_id, payload)


@taxes_router.delete(
    "/{tax_id}",
    response={
        HTTPStatus.OK: ErrorSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
    },
)
def delete_tax(request, tax_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return service.delete_tax(jwt, tax_id)
