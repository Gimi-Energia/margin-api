import uuid

import pytest
from ninja.errors import HttpError

from apps.icms.models import NCM, NCMGroup
from apps.icms.services.ncm_service import NCMService


@pytest.fixture
def ncm_service():
    return NCMService()


@pytest.mark.django_db
def test_get_ncm_group_by_id(ncm_service):
    group = NCMGroup.objects.create(name="Group 1")
    fetched_group = ncm_service.get_ncm_group_by_id(group.id)
    assert fetched_group == group


@pytest.mark.django_db
def test_get_ncm_group_by_ncm_code(ncm_service):
    group = NCMGroup.objects.create(name="Group 2")
    ncm = NCM.objects.create(code="12345678", group=group)
    fetched_group = ncm_service.get_ncm_group_by_ncm_code("12345678")
    assert fetched_group == group


@pytest.mark.django_db
def test_list_ncm_groups(ncm_service):
    NCMGroup.objects.create(name="Group 3")
    groups = ncm_service.list_ncm_groups()
    assert groups["count"] == 1
    assert groups["ncm_groups"][0].name == "Group 3"


@pytest.mark.django_db
def test_get_ncm_group_not_found(ncm_service):
    with pytest.raises(HttpError):
        ncm_service.get_ncm_group(uuid.uuid4())
