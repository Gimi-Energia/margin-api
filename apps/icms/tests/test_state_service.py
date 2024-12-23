import uuid

import pytest
from ninja.errors import HttpError

from apps.icms.models import State
from apps.icms.services.state_service import StateService


@pytest.fixture
def state_service():
    return StateService()


@pytest.fixture
def jwt():
    return {"is_margin_admin": True}


@pytest.mark.django_db
def test_get_state_by_id(state_service):
    state = State.objects.create(name="São Paulo", code="SP")
    fetched_state = state_service.get_state_by_id(state.id)
    assert fetched_state == state


@pytest.mark.django_db
def test_get_state_by_code(state_service):
    state = State.objects.create(name="Rio de Janeiro", code="RJ")
    fetched_state = state_service.get_state_by_code("RJ")
    assert fetched_state == state


@pytest.mark.django_db
def test_list_states(state_service):
    State.objects.create(name="Minas Gerais", code="MG")
    states = state_service.list_states()
    assert states["count"] == 1
    assert states["states"][0].code == "MG"


@pytest.mark.django_db
def test_get_state_not_found(state_service):
    with pytest.raises(HttpError):
        state_service.get_state(uuid.uuid4())
