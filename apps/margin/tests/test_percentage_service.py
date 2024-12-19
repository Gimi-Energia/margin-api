import uuid

import pytest
from ninja.errors import HttpError

from apps.margin.models import Percentage
from apps.margin.services.percentage_service import PercentageService


@pytest.fixture
def percentage_service():
    return PercentageService()


@pytest.mark.django_db
def test_get_percentage_by_id(percentage_service):
    percentage = Percentage.objects.create(value=10.0)
    fetched_percentage = percentage_service.get_percentage_by_id(percentage.id)
    assert fetched_percentage == percentage


@pytest.mark.django_db
def test_list_percentages(percentage_service):
    Percentage.objects.create(value=15.0)
    percentages = percentage_service.list_percentages()
    assert percentages["count"] == 1
    assert percentages["percentages"][0].value == 15.0


@pytest.mark.django_db
def test_get_percentage_not_found(percentage_service):
    with pytest.raises(HttpError):
        percentage_service.get_percentage(uuid.uuid4())
