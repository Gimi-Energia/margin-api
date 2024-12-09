import uuid

from django.shortcuts import get_object_or_404

from .models import NCM, ICMSRate, NCMGroup, State
from .schema import (
    ICMSRateCreateSchema,
    ICMSRateUpdateSchema,
    NCMGroupCreateSchema,
    NCMSCreateSchema,
    NCMSUpdateSchema,
)


class ICMSService:
    @staticmethod
    def list_states():
        return State.objects.all()

    @staticmethod
    def get_state(state_id: uuid.UUID):
        return get_object_or_404(State, id=state_id)

    @staticmethod
    def list_ncm_groups():
        return NCMGroup.objects.prefetch_related("ncms").all()

    @staticmethod
    def get_ncm_group(group_id: uuid.UUID):
        return get_object_or_404(NCMGroup, id=group_id)

    @staticmethod
    def create_ncm_group(payload: NCMGroupCreateSchema):
        return NCMGroup.objects.create(**payload.dict())

    @staticmethod
    def update_ncm_group(group_id: uuid.UUID, payload: NCMGroupCreateSchema):
        group = get_object_or_404(NCMGroup, id=group_id)
        for attr, value in payload.dict().items():
            setattr(group, attr, value)
        group.save()
        return group

    @staticmethod
    def create_ncm(payload: NCMSCreateSchema):
        group = NCMGroup.objects.get(id=payload.group)
        return NCM.objects.create(code=payload.code, group=group)

    @staticmethod
    def list_ncms():
        return NCM.objects.all()

    @staticmethod
    def get_ncm(ncm_id: uuid.UUID):
        return get_object_or_404(NCM, id=ncm_id)

    @staticmethod
    def update_ncm(ncm_id: uuid.UUID, payload: NCMSUpdateSchema):
        ncm = get_object_or_404(NCM, id=ncm_id)

        if payload.code is not None:
            ncm.code = payload.code

        if payload.group is not None:
            ncm.group = get_object_or_404(NCMGroup, id=payload.group)

        ncm.save()
        return ncm

    @staticmethod
    def create_icms_rate(payload: ICMSRateCreateSchema):
        state = get_object_or_404(State, id=payload.state)
        group = get_object_or_404(NCMGroup, id=payload.group)

        return ICMSRate.objects.create(
            state=state,
            group=group,
            internal_rate=payload.internal_rate,
            difal_rate=payload.difal_rate,
            poverty_rate=payload.poverty_rate,
        )

    @staticmethod
    def list_icms_rates():
        return ICMSRate.objects.select_related("state", "group").all()

    @staticmethod
    def get_icms_rate(rate_id: uuid.UUID):
        return get_object_or_404(ICMSRate, id=rate_id)

    @staticmethod
    def update_icms_rate(rate_id: uuid.UUID, payload: ICMSRateUpdateSchema):
        rate = get_object_or_404(ICMSRate, id=rate_id)

        if payload.state is not None:
            rate.state = get_object_or_404(State, id=payload.state)

        if payload.group is not None:
            rate.group = get_object_or_404(NCMGroup, id=payload.group)

        if payload.internal_rate is not None:
            rate.internal_rate = payload.internal_rate

        if payload.difal_rate is not None:
            rate.difal_rate = payload.difal_rate

        if payload.poverty_rate is not None:
            rate.poverty_rate = payload.poverty_rate

        rate.save()

        return rate
