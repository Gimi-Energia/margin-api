import uuid
from http import HTTPStatus

from ninja.errors import HttpError

from apps.icms.models import State


class StateService:
    @staticmethod
    def get_state_by_id(state_id: uuid.UUID):
        return State.objects.filter(pk=state_id).first()

    def get_states_by_ids(self, state_ids: list[uuid.UUID]):
        return State.objects.filter(id__in=state_ids)

    @staticmethod
    def get_state_by_code(state_code: str):
        return State.objects.filter(code=state_code).first()

    @staticmethod
    def list_states():
        states = State.objects.all()
        count = states.count()
        return {"count": count, "states": states}

    def get_state(self, state_id: uuid.UUID):
        if not (state := self.get_state_by_id(state_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Estado não encontrado")

        return state
