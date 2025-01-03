import uuid

from ninja import Router

from apps.icms.schema import (
    ICMSRateBulkCreateSchema,
    ICMSRateCreateSchema,
    ICMSRateListSchema,
    ICMSRateSchema,
    ICMSRateUpdateSchema,
    NCMGroupCreateSchema,
    NCMGroupListSchema,
    NCMGroupSchema,
    NCMSchema,
    NCMSCreateSchema,
    NCMSListchema,
    NCMSUpdateSchema,
    StateListSchema,
    StateSchema,
)
from apps.icms.services.icms_service import ICMSService
from apps.icms.services.ncm_service import NCMService
from apps.icms.services.state_service import StateService
from utils.jwt import JWTAuth, decode_jwt_token

icms_router = Router(auth=JWTAuth())
icms_service = ICMSService()

ncm_router = Router(auth=JWTAuth())
ncm_service = NCMService()

state_router = Router(auth=JWTAuth())
state_service = StateService()


@state_router.get("", response=StateListSchema)
def list_states(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return state_service.list_states()


@state_router.get("/{state_id}", response=StateSchema)
def get_state(request, state_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return state_service.get_state(state_id)


@ncm_router.post("/groups", response=NCMGroupSchema)
def create_ncm_group(request, payload: NCMGroupCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.create_ncm_group(jwt, payload)


@ncm_router.get("/groups", response=NCMGroupListSchema)
def list_ncm_groups(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.list_ncm_groups()


@ncm_router.get("/groups/{group_id}", response=NCMGroupSchema)
def get_ncm_group(request, group_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.get_ncm_group(group_id)


@ncm_router.patch("/groups/{group_id}", response=NCMGroupSchema)
def update_ncm_group(request, group_id: uuid.UUID, payload: NCMGroupCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.update_ncm_group(jwt, group_id, payload)


@ncm_router.delete("/groups/{group_id}")
def delete_ncm_group(request, group_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.delete_ncm_group(jwt, group_id)


@ncm_router.post("", response=NCMSchema)
def create_ncm(request, payload: NCMSCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.create_ncm(jwt, payload)


@ncm_router.get("", response=NCMSListchema)
def list_ncms(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.list_ncms()


@ncm_router.get("/{ncm_id}", response=NCMSchema)
def get_ncm(request, ncm_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.get_ncm(ncm_id)


@ncm_router.patch("/{ncm_id}", response=NCMSchema)
def update_ncm(request, ncm_id: uuid.UUID, payload: NCMSUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.update_ncm(jwt, ncm_id, payload)


@ncm_router.delete("/{ncm_id}")
def delete_ncm(request, ncm_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return ncm_service.delete_ncm(jwt, ncm_id)


@icms_router.post("/rates", response=ICMSRateSchema)
def create_icms_rate(request, payload: ICMSRateCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.create_icms_rate(jwt, payload)


@icms_router.get("/rates", response=ICMSRateListSchema)
def list_icms_rates(request):
    decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.list_icms_rates()


@icms_router.post("/rates/bulk-create")
def bulk_create_icms_rates(request, payload: ICMSRateBulkCreateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.bulk_create_icms_rates(jwt, payload)


@icms_router.get("/rates/{icms_rate_id}", response=ICMSRateSchema)
def get_icms_rate(request, icms_rate_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.get_icms_rate(icms_rate_id)


@icms_router.patch("/rates/{icms_rate_id}", response=ICMSRateSchema)
def update_icms_rate(request, icms_rate_id: uuid.UUID, payload: ICMSRateUpdateSchema):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.update_icms_rate(jwt, icms_rate_id, payload)


@icms_router.delete("/rates/{icms_rate_id}")
def delete_icms_rate(request, icms_rate_id: uuid.UUID):
    jwt = decode_jwt_token(request.headers.get("Authorization"))
    return icms_service.delete_icms_rate(jwt, icms_rate_id)
