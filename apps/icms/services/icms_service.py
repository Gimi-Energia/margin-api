import uuid
from http import HTTPStatus

from ninja.errors import HttpError

from apps.icms.models import ICMSRate
from apps.icms.schema import ICMSRateCreateSchema, ICMSRateUpdateSchema
from apps.icms.services.ncm_service import NCMService
from apps.icms.services.state_service import StateService


class ICMSService:
    @property
    def ncm_service(self):
        return NCMService()

    @property
    def state_service(self):
        return StateService()

    def create_icms_rate(self, payload: ICMSRateCreateSchema):
        if not (state := self.state_service.get_state_by_id(payload.state)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

        if not (ncm_group := self.ncm_service.get_ncm_group_by_id(payload.group)):
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
            if not (state := self.state_service.get_state_by_id(payload.state)):
                raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

            icms_rate.state = state

        if payload.group is not None:
            if not (ncm_group := self.ncm_service.get_ncm_group_by_id(payload.group)):
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
