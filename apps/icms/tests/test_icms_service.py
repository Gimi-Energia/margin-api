import uuid

import pytest
from ninja.errors import HttpError

from apps.icms.models import ICMSRate, NCMGroup, State
from apps.icms.schema import ICMSRateCreateSchema
from apps.icms.services.icms_service import ICMSService


@pytest.fixture
def icms_service():
    return ICMSService()


@pytest.mark.django_db
def test_create_icms_rate(icms_service):
    state = State.objects.create(name="Paraná", code="PR")
    group = NCMGroup.objects.create(name="Group 4")
    payload = {
        "state": state.id,
        "group": group.id,
        "internal_rate": 18.0,
        "difal_rate": 2.0,
        "poverty_rate": 1.0,
    }
    icms_rate_schema = ICMSRateCreateSchema(**payload)
    icms_rate = icms_service.create_icms_rate(icms_rate_schema)
    assert icms_rate.state == state
    assert icms_rate.group == group
    assert icms_rate.internal_rate == 18.0


@pytest.mark.django_db
def test_get_icms_rate_by_id(icms_service):
    state = State.objects.create(name="Santa Catarina", code="SC")
    group = NCMGroup.objects.create(name="Group 5")
    icms_rate = ICMSRate.objects.create(
        state=state, group=group, internal_rate=17.0, difal_rate=3.0, poverty_rate=1.5
    )
    fetched_rate = icms_service.get_icms_rate_by_id(icms_rate.id)
    assert fetched_rate == icms_rate


@pytest.mark.django_db
def test_list_icms_rates(icms_service):
    state = State.objects.create(name="Bahia", code="BA")
    group = NCMGroup.objects.create(name="Group 6")
    ICMSRate.objects.create(
        state=state, group=group, internal_rate=16.0, difal_rate=2.5, poverty_rate=1.0
    )
    rates = icms_service.list_icms_rates()
    assert rates["count"] == 1
    assert rates["icms_rates"][0].state.code == "BA"


@pytest.mark.django_db
def test_get_icms_rate_not_found(icms_service):
    with pytest.raises(HttpError):
        icms_service.get_icms_rate(uuid.uuid4())
