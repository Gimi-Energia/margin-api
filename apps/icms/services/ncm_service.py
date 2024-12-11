import uuid
from http import HTTPStatus
from django.http import JsonResponse

from ninja.errors import HttpError

from apps.icms.models import NCM, NCMGroup
from apps.icms.schema import NCMGroupCreateSchema, NCMSCreateSchema, NCMSUpdateSchema


class NCMService:
    @staticmethod
    def get_ncm_group_by_id(ncm_group_id: uuid.UUID):
        return NCMGroup.objects.filter(pk=ncm_group_id).first()

    @staticmethod
    def list_ncm_groups():
        ncm_groups = NCMGroup.objects.prefetch_related("ncms").all()
        count = ncm_groups.count()
        return {"count": count, "ncm_groups": ncm_groups}

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

        for attr, value in payload.model_dump(
            exclude_defaults=True, exclude_unset=True
        ).items():
            setattr(ncm_group, attr, value)
        ncm_group.save()
        return ncm_group

    def delete_ncm_group(self, ncm_group_id: uuid.UUID):
        if not (ncm_group := self.get_ncm_group_by_id(ncm_group_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

        ncm_group.delete()
        return JsonResponse(
            {"detail": "Grupo de NCM deletado com sucesso"}, status=HTTPStatus.OK
        )

    def create_ncm(self, payload: NCMSCreateSchema):
        if not (ncm_group := self.get_ncm_group_by_id(payload.group)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

        return NCM.objects.create(code=payload.code, group=ncm_group)

    @staticmethod
    def get_ncm_by_id(ncm_id: uuid.UUID):
        return NCM.objects.filter(pk=ncm_id).first()

    @staticmethod
    def get_ncm_by_code(ncm_code: str):
        return NCM.objects.filter(code=ncm_code).first()

    @staticmethod
    def list_ncms():
        ncms = NCM.objects.all()
        count = ncms.count()
        return {"count": count, "ncms": ncms}

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

    def delete_ncm(self, ncm_id: uuid.UUID):
        if not (ncm := self.get_ncm_by_id(ncm_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "NCM não encontrado")

        ncm.delete()
        return JsonResponse(
            {"detail": "NCM deletado com sucesso"}, status=HTTPStatus.OK
        )
