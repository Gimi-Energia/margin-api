import uuid
from http import HTTPStatus

from django.http import JsonResponse
from ninja.errors import HttpError

from apps.icms.models import ICMSRate
from apps.icms.schema import (
    ICMSRateBulkCreateSchema,
    ICMSRateCreateSchema,
    ICMSRateUpdateSchema,
)
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

    def bulk_create_icms_rates(self, payload: ICMSRateBulkCreateSchema):
        if not (rates := payload.rates):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Nenhum dado enviado.")

        group_id = rates[0].group
        if not (ncm_group := self.ncm_service.get_ncm_group_by_id(group_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado.")

        for rate in rates:
            if rate.group != group_id:
                raise HttpError(
                    HTTPStatus.BAD_REQUEST,
                    "Todos os registros devem usar o mesmo grupo de NCM.",
                )
            if not rate.internal_rate or not rate.difal_rate or not rate.poverty_rate:
                raise HttpError(HTTPStatus.BAD_REQUEST, "As taxas não podem ser nulas.")

        all_states_data = self.state_service.list_states()
        all_states = all_states_data["states"]
        all_state_codes = {state.code for state in all_states}

        rates_state_codes = {
            next(
                (state.code for state in all_states if state.id == item.state),
                None,
            )
            for item in rates
        }

        if missing_states := all_state_codes - rates_state_codes:
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                f"Os seguintes estados não foram enviados: {', '.join(missing_states)}",
            )

        rates_to_create = []
        for rate in rates:
            if not (state := next((s for s in all_states if s.id == rate.state), None)):
                raise HttpError(
                    HTTPStatus.NOT_FOUND,
                    f"Estado com ID {rate.state} não encontrado.",
                )
            rates_to_create.append(
                ICMSRate(
                    state=state,
                    group=ncm_group,
                    internal_rate=rate.internal_rate,
                    difal_rate=rate.difal_rate,
                    poverty_rate=rate.poverty_rate,
                )
            )

        ICMSRate.objects.bulk_create(rates_to_create)

        return JsonResponse(
            {"detail": f"{len(rates_to_create)} registros criados com sucesso"},
            status=HTTPStatus.OK,
        )

    @staticmethod
    def get_icms_rate_by_id(icms_rate_id: uuid.UUID):
        return ICMSRate.objects.filter(pk=icms_rate_id).first()

    def get_rate_by_state_and_ncm(self, state_code: str, ncm_code: str):
        if not (state := self.state_service.get_state_by_code(state_code)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

        if not (ncm := self.ncm_service.get_ncm_by_code(ncm_code)):
            raise HttpError(HTTPStatus.NOT_FOUND, "NCM não encontrado")

        group = ncm.group

        return ICMSRate.objects.filter(state=state, group=group).first()

    @staticmethod
    def list_icms_rates():
        icms_rates = ICMSRate.objects.select_related("state", "group").all()
        count = icms_rates.count()
        return {"count": count, "icms_rates": icms_rates}

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

    def delete_icms_rate(self, icms_rate_id: uuid.UUID):
        if not (icms_rate := self.get_icms_rate_by_id(icms_rate_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Taxa de ICMS não encontrada")

        icms_rate.delete()
        return JsonResponse(
            {"detail": "Taxa de ICMS deletada com sucesso"}, status=HTTPStatus.OK
        )
