import uuid
from http import HTTPStatus

from ninja import Router

from apps.icms.schema import (
    ICMSRateBulkCreateSchema,
    ICMSRateBulkUpdateSchema,
    ICMSRateCreateSchema,
    ICMSRateListSchema,
    ICMSRateSchema,
    ICMSRateUpdateSchema,
    NCMGroupCreateSchema,
    NCMGroupListSchema,
    NCMGroupSchema,
    NCMSchema,
    NCMSchemaWithGroup,
    NCMSCreateSchema,
    NCMSListchema,
    NCMSUpdateSchema,
    StateListSchema,
    StateSchema,
)
from apps.icms.services.icms_service import ICMSService
from apps.icms.services.ncm_service import NCMService
from apps.icms.services.state_service import StateService
from utils.base_schema import ErrorSchema
from utils.jwt import JWTAuth, decode_jwt_token

icms_router = Router(auth=JWTAuth())
icms_service = ICMSService()

ncm_router = Router(auth=JWTAuth())
ncm_service = NCMService()

state_router = Router(auth=JWTAuth())
state_service = StateService()


@state_router.get(
    "", response={HTTPStatus.OK: StateListSchema, HTTPStatus.FORBIDDEN: ErrorSchema}
)
def list_states(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return state_service.list_states()


@state_router.get(
    "/{state_id}",
    response={
        HTTPStatus.OK: StateSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def get_state(request, state_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return state_service.get_state(state_id)


@ncm_router.post(
    "/groups",
    response={
        HTTPStatus.CREATED: NCMGroupSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_ncm_group(request, payload: NCMGroupCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.create_ncm_group(jwt, payload)


@ncm_router.get(
    "/groups",
    response={HTTPStatus.OK: NCMGroupListSchema, HTTPStatus.FORBIDDEN: ErrorSchema},
)
def list_ncm_groups(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.list_ncm_groups()


@ncm_router.get(
    "/groups/{group_id}",
    response={
        HTTPStatus.OK: NCMGroupSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def get_ncm_group(request, group_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.get_ncm_group(group_id)


@ncm_router.patch(
    "/groups/{group_id}",
    response={
        HTTPStatus.OK: NCMGroupSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def update_ncm_group(request, group_id: uuid.UUID, payload: NCMGroupCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.update_ncm_group(jwt, group_id, payload)


@ncm_router.delete(
    "/groups/{group_id}",
    response={
        HTTPStatus.OK: ErrorSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
    },
)
def delete_ncm_group(request, group_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.delete_ncm_group(jwt, group_id)


@ncm_router.post(
    "",
    response={
        HTTPStatus.CREATED: NCMSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_ncm(request, payload: NCMSCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.create_ncm(jwt, payload)


@ncm_router.get(
    "", response={HTTPStatus.OK: NCMSListchema, HTTPStatus.FORBIDDEN: ErrorSchema}
)
def list_ncms(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.list_ncms()


@ncm_router.get(
    "/{ncm_id}",
    response={
        HTTPStatus.OK: NCMSchemaWithGroup,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def get_ncm(request, ncm_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.get_ncm(ncm_id)


@ncm_router.patch(
    "/{ncm_id}",
    response={
        HTTPStatus.OK: NCMSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def update_ncm(request, ncm_id: uuid.UUID, payload: NCMSUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.update_ncm(jwt, ncm_id, payload)


@ncm_router.delete(
    "/{ncm_id}",
    response={
        HTTPStatus.OK: ErrorSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
    },
)
def delete_ncm(request, ncm_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.delete_ncm(jwt, ncm_id)


@icms_router.post(
    "/rates",
    response={
        HTTPStatus.CREATED: ICMSRateSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def create_icms_rate(request, payload: ICMSRateCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.create_icms_rate(jwt, payload)


@icms_router.get(
    "/rates",
    response={HTTPStatus.OK: ICMSRateListSchema, HTTPStatus.FORBIDDEN: ErrorSchema},
)
def list_icms_rates(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.list_icms_rates()


@icms_router.get(
    "/rates/group/{group_id}",
    response={HTTPStatus.OK: ICMSRateListSchema, HTTPStatus.FORBIDDEN: ErrorSchema},
)
def list_icms_rates_by_group(request, group_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.list_icms_rates_by_group(group_id)


@icms_router.post(
    "/rates/bulk-create",
    response={
        HTTPStatus.OK: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def bulk_create_icms_rates(request, payload: ICMSRateBulkCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.bulk_create_icms_rates(jwt, payload)


@icms_router.patch(
    "/rates/bulk-update",
    response={
        HTTPStatus.OK: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def bulk_update_icms_rates(request, payload: ICMSRateBulkUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.bulk_update_icms_rates(jwt, payload)


@icms_router.get(
    "/rates/{icms_rate_id}",
    response={
        HTTPStatus.OK: ICMSRateSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
    },
)
def get_icms_rate(request, icms_rate_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.get_icms_rate(icms_rate_id)


@icms_router.patch(
    "/rates/{icms_rate_id}",
    response={
        HTTPStatus.OK: ICMSRateSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
        HTTPStatus.INTERNAL_SERVER_ERROR: ErrorSchema,
    },
)
def update_icms_rate(request, icms_rate_id: uuid.UUID, payload: ICMSRateUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.update_icms_rate(jwt, icms_rate_id, payload)


@icms_router.delete(
    "/rates/{icms_rate_id}",
    response={
        HTTPStatus.OK: ErrorSchema,
        HTTPStatus.NOT_FOUND: ErrorSchema,
        HTTPStatus.FORBIDDEN: ErrorSchema,
        HTTPStatus.BAD_REQUEST: ErrorSchema,
    },
)
def delete_icms_rate(request, icms_rate_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.delete_icms_rate(jwt, icms_rate_id)
