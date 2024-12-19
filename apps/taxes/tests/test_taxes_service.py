import uuid

import pytest
from ninja.errors import HttpError

from apps.taxes.models import Tax
from apps.taxes.service import TaxesService


@pytest.fixture
def taxes_service():
    return TaxesService()


@pytest.mark.django_db
def test_get_tax_by_id(taxes_service):
    tax = Tax.objects.create(
        name="Tax 1", presumed_profit_rate=10.0, real_profit_rate=15.0
    )
    fetched_tax = taxes_service.get_tax_by_id(tax.id)
    assert fetched_tax == tax


@pytest.mark.django_db
def test_list_taxes(taxes_service):
    Tax.objects.create(name="Tax 2", presumed_profit_rate=12.0, real_profit_rate=18.0)
    taxes = taxes_service.list_taxes()
    assert taxes["count"] == 1
    assert taxes["taxes"][0].name == "Tax 2"


@pytest.mark.django_db
def test_get_tax_not_found(taxes_service):
    with pytest.raises(HttpError):
        taxes_service.get_tax(uuid.uuid4())
