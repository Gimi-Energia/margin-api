import uuid
from http import HTTPStatus

from ninja.errors import HttpError

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
    def get_state_by_id(state_id: uuid.UUID):
        return State.objects.filter(pk=state_id).first()

    @staticmethod
    def list_states():
        states = State.objects.all()
        total = states.count()
        return {"total": total, "states": states}

    def get_state(self, state_id: uuid.UUID):
        if not (state := self.get_state_by_id(state_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

        return state

    @staticmethod
    def get_ncm_group_by_id(ncm_group_id: uuid.UUID):
        return NCMGroup.objects.filter(pk=ncm_group_id).first()

    @staticmethod
    def list_ncm_groups():
        ncm_groups = NCMGroup.objects.prefetch_related("ncms").all()
        total = ncm_groups.count()
        return {"total": total, "ncm_groups": ncm_groups}

    def get_ncm_group(self, group_id: uuid.UUID):
        if not (ncm_group := self.get_ncm_group_by_id(group_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

        return ncm_group

    @staticmethod
    def create_ncm_group(payload: NCMGroupCreateSchema):
        return NCMGroup.objects.create(**payload.dict())

    def update_ncm_group(self, group_id: uuid.UUID, payload: NCMGroupCreateSchema):
        if not (ncm_group := self.get_ncm_group_by_id(group_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

        for attr, value in payload.dict().items():
            setattr(ncm_group, attr, value)
        ncm_group.save()
        return ncm_group

    def create_ncm(self, payload: NCMSCreateSchema):
        if not (ncm_group := self.get_ncm_group_by_id(payload.group)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

        return NCM.objects.create(code=payload.code, group=ncm_group)

    @staticmethod
    def get_ncm_by_id(ncm_id: uuid.UUID):
        return NCM.objects.filter(pk=ncm_id).first()

    @staticmethod
    def list_ncms():
        ncms = NCM.objects.all()
        total = ncms.count()
        return {"total": total, "ncms": ncms}

    def get_ncm(self, ncm_id: uuid.UUID):
        if not (ncm := self.get_ncm_by_id(ncm_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "NCM não encontrado")

        return ncm

    def update_ncm(self, ncm_id: uuid.UUID, payload: NCMSUpdateSchema):
        if not (ncm := self.get_ncm_by_id(ncm_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "NCM não encontrado")

        if payload.code is not None:
            ncm.code = payload.code

        if payload.group is not None:
            if not (ncm_group := self.get_ncm_group_by_id(payload.group)):
                raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

            ncm.group = ncm_group

        ncm.save()
        return ncm

    def create_icms_rate(self, payload: ICMSRateCreateSchema):
        if not (state := self.get_state_by_id(payload.state)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

        if not (ncm_group := self.get_ncm_group_by_id(payload.group)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

        return ICMSRate.objects.create(
            state=state,
            group=ncm_group,
            internal_rate=payload.internal_rate,
            difal_rate=payload.difal_rate,
            poverty_rate=payload.poverty_rate,
        )

    @staticmethod
    def get_icms_rate_by_id(icms_rate_id: uuid.UUID):
        return ICMSRate.objects.filter(pk=icms_rate_id).first()

    @staticmethod
    def list_icms_rates():
        icms_rates = ICMSRate.objects.select_related("state", "group").all()
        total = icms_rates.count()
        return {"total": total, "icms_rates": icms_rates}

    def get_icms_rate(self, icms_rate_id: uuid.UUID):
        if not (icms_rate := self.get_icms_rate_by_id(icms_rate_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Taxa de ICMS não encontrada")

        return icms_rate

    def update_icms_rate(self, icms_rate_id: uuid.UUID, payload: ICMSRateUpdateSchema):
        if not (icms_rate := self.get_icms_rate_by_id(icms_rate_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Taxa de ICMS não encontrada")

        if payload.state is not None:
            if not (state := self.get_state_by_id(payload.state)):
                raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

            icms_rate.state = state

        if payload.group is not None:
            if not (ncm_group := self.get_ncm_group_by_id(payload.group)):
                raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

            icms_rate.group = ncm_group

        if payload.internal_rate is not None:
            icms_rate.internal_rate = payload.internal_rate

        if payload.difal_rate is not None:
            icms_rate.difal_rate = payload.difal_rate

        if payload.poverty_rate is not None:
            icms_rate.poverty_rate = payload.poverty_rate

        icms_rate.save()

        return icms_rate
