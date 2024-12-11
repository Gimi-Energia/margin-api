import uuid

from ninja import Router

from apps.icms.schema import (
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

icms_router = Router()
icms_service = ICMSService()

ncm_router = Router()
ncm_service = NCMService()

state_router = Router()
state_service = StateService()


@state_router.get("", response=StateListSchema)
def list_states(request):
    return state_service.list_states()


@state_router.get("/{state_id}", response=StateSchema)
def get_state(request, state_id: uuid.UUID):
    return state_service.get_state(state_id)


@ncm_router.post("/groups", response=NCMGroupSchema)
def create_ncm_group(request, payload: NCMGroupCreateSchema):
    return ncm_service.create_ncm_group(payload)


@ncm_router.get("/groups", response=NCMGroupListSchema)
def list_ncm_groups(request):
    return ncm_service.list_ncm_groups()


@ncm_router.get("/groups/{group_id}", response=NCMGroupSchema)
def get_ncm_group(request, group_id: uuid.UUID):
    return ncm_service.get_ncm_group(group_id)


@ncm_router.patch("/groups/{group_id}", response=NCMGroupSchema)
def update_ncm_group(request, group_id: uuid.UUID, payload: NCMGroupCreateSchema):
    return ncm_service.update_ncm_group(group_id, payload)


@ncm_router.delete("/groups/{group_id}")
def delete_ncm_group(request, group_id: uuid.UUID):
    return ncm_service.delete_ncm_group(group_id)


@ncm_router.post("", response=NCMSchema)
def create_ncm(request, payload: NCMSCreateSchema):
    return ncm_service.create_ncm(payload)


@ncm_router.get("", response=NCMSListchema)
def list_ncms(request):
    return ncm_service.list_ncms()


@ncm_router.get("/{ncm_id}", response=NCMSchema)
def get_ncm(request, ncm_id: uuid.UUID):
    return ncm_service.get_ncm(ncm_id)


@ncm_router.patch("/{ncm_id}", response=NCMSchema)
def update_ncm(request, ncm_id: uuid.UUID, payload: NCMSUpdateSchema):
    return ncm_service.update_ncm(ncm_id, payload)


@ncm_router.delete("/{ncm_id}")
def delete_ncm(request, ncm_id: uuid.UUID):
    return ncm_service.delete_ncm(ncm_id)


@icms_router.post("/rates", response=ICMSRateSchema)
def create_icms_rate(request, payload: ICMSRateCreateSchema):
    return icms_service.create_icms_rate(payload)


@icms_router.get("/rates", response=ICMSRateListSchema)
def list_icms_rates(request):
    return icms_service.list_icms_rates()


@icms_router.get("/rates/{icms_rate_id}", response=ICMSRateSchema)
def get_icms_rate(request, icms_rate_id: uuid.UUID):
    return icms_service.get_icms_rate(icms_rate_id)


@icms_router.patch("/rates/{icms_rate_id}", response=ICMSRateSchema)
def update_icms_rate(request, icms_rate_id: uuid.UUID, payload: ICMSRateUpdateSchema):
    return icms_service.update_icms_rate(icms_rate_id, payload)


@icms_router.delete("/rates/{icms_rate_id}")
def delete_icms_rate(request, icms_rate_id: uuid.UUID):
    return icms_service.delete_icms_rate(icms_rate_id)
