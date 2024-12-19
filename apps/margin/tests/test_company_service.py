import uuid

import pytest
from ninja.errors import HttpError

from apps.margin.models import Company
from apps.margin.services.company_service import CompanyService


@pytest.fixture
def company_service():
    return CompanyService()


@pytest.mark.django_db
def test_get_company_by_id(company_service):
    company = Company.objects.create(name="Test Company", profit_type="real")
    fetched_company = company_service.get_company_by_id(company.id)
    assert fetched_company == company


@pytest.mark.django_db
def test_list_companies(company_service):
    Company.objects.create(name="Test Company", profit_type="real")
    companies = company_service.list_companies()
    assert companies["count"] == 1
    assert companies["companies"][0].name == "Test Company"


@pytest.mark.django_db
def test_get_company_not_found(company_service):
    with pytest.raises(HttpError):
        company_service.get_company(uuid.uuid4())
