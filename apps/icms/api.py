import uuid

from ninja import Router

from .schema import (
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
from .service import ICMSService

icms_router = Router()
service = ICMSService()


@icms_router.get("/states", response=StateListSchema)
def list_states(request):
    return service.list_states()


@icms_router.get("/states/{state_id}", response=StateSchema)
def get_state(request, state_id: uuid.UUID):
    return service.get_state(state_id)


@icms_router.post("/ncm-groups", response=NCMGroupSchema)
def create_ncm_group(request, payload: NCMGroupCreateSchema):
    return service.create_ncm_group(payload)


@icms_router.get("/ncm-groups", response=NCMGroupListSchema)
def list_ncm_groups(request):
    return service.list_ncm_groups()


@icms_router.get("/ncm-groups/{group_id}", response=NCMGroupSchema)
def get_ncm_group(request, group_id: uuid.UUID):
    return service.get_ncm_group(group_id)


@icms_router.patch("/ncm-groups/{group_id}", response=NCMGroupSchema)
def update_ncm_group(request, group_id: uuid.UUID, payload: NCMGroupCreateSchema):
    return service.update_ncm_group(group_id, payload)


@icms_router.post("/ncm", response=NCMSchema)
def create_ncm(request, payload: NCMSCreateSchema):
    return service.create_ncm(payload)


@icms_router.get("/ncm", response=NCMSListchema)
def list_ncms(request):
    return service.list_ncms()


@icms_router.get("/ncm/{ncm_id}", response=NCMSchema)
def get_ncm(request, ncm_id: uuid.UUID):
    return service.get_ncm(ncm_id)


@icms_router.patch("/ncm/{ncm_id}", response=NCMSchema)
def update_ncm(request, ncm_id: uuid.UUID, payload: NCMSUpdateSchema):
    return service.update_ncm(ncm_id, payload)


@icms_router.post("/rates", response=ICMSRateSchema)
def create_icms_rate(request, payload: ICMSRateCreateSchema):
    return service.create_icms_rate(payload)


@icms_router.get("/rates", response=ICMSRateListSchema)
def list_icms_rates(request):
    return service.list_icms_rates()


@icms_router.get("/rates/{icms_rate_id}", response=ICMSRateSchema)
def get_icms_rate(request, icms_rate_id: uuid.UUID):
    return service.get_icms_rate(icms_rate_id)


@icms_router.patch("/rates/{icms_rate_id}", response=ICMSRateSchema)
def update_icms_rate(request, icms_rate_id: uuid.UUID, payload: ICMSRateUpdateSchema):
    return service.update_icms_rate(icms_rate_id, payload)
