import uuid
from http import HTTPStatus

from ninja import Router

from apps.margin.schema import (
    CompanyCreateSchema,
    CompanyListSchema,
    CompanySchema,
    CompanyUpdateSchema,
    ContractCalculateSchema,
    ContractFindSchema,
    ContractReturnSchema,
    PercentageListSchema,
    PercentageSchema,
    PercentageUpdateSchema,
)
from apps.margin.services.company_service import CompanyService
from apps.margin.services.contract_service import ContractService
from apps.margin.services.percentage_service import PercentageService
from utils.base_schema import ErrorSchema
from utils.jwt import JWTAuth, decode_jwt_token

company_router = Router(auth=JWTAuth())
company_service = CompanyService()

percentage_router = Router(auth=JWTAuth())
percentage_service = PercentageService()

contract_router = Router(auth=JWTAuth())
contract_service = ContractService()


@company_router.post(
    "",
    response={
        HTTPStatus.OK: CompanySchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_company(request, payload: CompanyCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return company_service.create_company(jwt, payload)


@company_router.get(
    "", response={HTTPStatus.OK: CompanyListSchema, HTTPStatus.FORBIDDEN: ErrorSchema}
)
def list_companies(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return company_service.list_companies()


@company_router.get(
    "/{company_id}",
    response={
        HTTPStatus.OK: CompanySchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def get_company(request, company_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return company_service.get_company(company_id)


@company_router.patch(
    "/{company_id}",
    response={
        HTTPStatus.OK: CompanySchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def update_company(request, company_id: uuid.UUID, payload: CompanyUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return company_service.update_company(jwt, company_id, payload)


@company_router.delete(
    "/{company_id}",
    response={
        HTTPStatus.OK: ErrorSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
    },
)
def delete_company(request, company_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return company_service.delete_company(jwt, company_id)


@percentage_router.get(
    "",
    response={HTTPStatus.OK: PercentageListSchema, HTTPStatus.FORBIDDEN: ErrorSchema},
)
def list_percentages(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return percentage_service.list_percentages()


@percentage_router.get(
    "/{percentage_id}",
    response={
        HTTPStatus.OK: PercentageSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def get_percentage(request, percentage_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return percentage_service.get_percentage(percentage_id)


@percentage_router.patch(
    "/{percentage_id}",
    response={
        HTTPStatus.OK: PercentageSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def update_percentage(
    request, percentage_id: uuid.UUID, payload: PercentageUpdateSchema
):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return percentage_service.update_percentage(jwt, percentage_id, payload)


@contract_router.get(
    "/find",
    response={
        HTTPStatus.OK: ContractFindSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def find_iapp_contract(
    request,
    company_id: uuid.UUID,
    contract: str,
    is_end_consumer: bool,
    taxes_considered: str,
):
    decode_jwt_token(request.headers.get("Authorization"))
    return contract_service.find_iapp_contract(
        company_id, contract, is_end_consumer, taxes_considered
    )


@contract_router.get(
    "/calculate",
    response={
        HTTPStatus.OK: ContractCalculateSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def calculate_iapp_contract(
    request, contract_id: uuid.UUID, percentage_id: uuid.UUID, admin_rate: float
):
    decode_jwt_token(request.headers.get("Authorization"))
    return contract_service.calculate_iapp_contract(
        contract_id, percentage_id, admin_rate
    )


@contract_router.get(
    "/return",
    response={
        HTTPStatus.OK: ContractReturnSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def return_iapp_contract(request, contract_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    user_email = jwt.get("email")
    token = request.headers.get("Authorization").split(" ")[1]
    return contract_service.return_iapp_contract(contract_id, user_email, token)
