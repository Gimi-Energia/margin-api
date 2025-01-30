import uuid
from http import HTTPStatus

from django.db import IntegrityError
from django.http import JsonResponse
from ninja.errors import HttpError

from apps.icms.models import NCM, NCMGroup
from apps.icms.schema import NCMGroupCreateSchema, NCMSCreateSchema, NCMSUpdateSchema
from utils.validation import ValidationService


class NCMService:
    def __init__(self):
        self.validation_service = ValidationService()

    @staticmethod
    def get_ncm_group_by_id(ncm_group_id: uuid.UUID):
        return NCMGroup.objects.filter(pk=ncm_group_id).first()

    @staticmethod
    def get_ncm_group_by_ncm_code(ncm_code: str):
        if not (
            ncm := NCM.objects.filter(code=ncm_code).select_related("group").first()
        ):
            raise HttpError(
                HTTPStatus.NOT_FOUND, "NCM com o código especificado não encontrado"
            )
        return ncm.group

    @staticmethod
    def count_ncm_groups() -> int:
        return NCMGroup.objects.count()

    @staticmethod
    def list_ncm_groups():
        ncm_groups = NCMGroup.objects.prefetch_related("ncms").all()
        count = ncm_groups.count()
        return {"count": count, "ncm_groups": ncm_groups}

    def get_ncm_group(self, group_id: uuid.UUID):
        if not (ncm_group := self.get_ncm_group_by_id(group_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Grupo de NCM não encontrado")

        return ncm_group

    def create_ncm_group(self, jwt: dict, payload: NCMGroupCreateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        try:
            return NCMGroup.objects.create(**payload.dict())
        except IntegrityError as exc:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Grupo de NCM já existe") from exc

    def update_ncm_group(
        self, jwt: dict, group_id: uuid.UUID, payload: NCMGroupCreateSchema
    ):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        ncm_group = self.get_ncm_group(group_id)

        for attr, value in payload.model_dump(
            exclude_defaults=True, exclude_unset=True
        ).items():
            setattr(ncm_group, attr, value)

        try:
            ncm_group.save()
        except IntegrityError as exc:
            raise HttpError(HTTPStatus.BAD_REQUEST, "Grupo de NCM já existe") from exc

        return ncm_group

    def delete_ncm_group(self, jwt: dict, ncm_group_id: uuid.UUID):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        if self.count_ncm_groups() <= 1:
            raise HttpError(
                HTTPStatus.BAD_REQUEST, "Não é possível deletar o último grupo de NCM"
            )

        ncm_group = self.get_ncm_group(ncm_group_id)
        ncm_group.delete()

        return JsonResponse(
            {"detail": "Grupo de NCM deletado com sucesso"}, status=HTTPStatus.OK
        )

    def create_ncm(self, jwt: dict, payload: NCMSCreateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        if not self.validation_service.validate_ncm_code_format(payload.code):
            raise HttpError(HTTPStatus.BAD_REQUEST, "Código NCM no formato inválido")

        ncm_group = self.get_ncm_group(payload.group)

        try:
            return NCM.objects.create(code=payload.code, group=ncm_group)
        except IntegrityError as exc:
            raise HttpError(
                HTTPStatus.BAD_REQUEST, "NCM com o código especificado já existe"
            ) from exc

    @staticmethod
    def get_ncm_by_id(ncm_id: uuid.UUID):
        return NCM.objects.filter(pk=ncm_id).first()

    @staticmethod
    def get_ncm_by_code(ncm_code: str):
        return NCM.objects.filter(code=ncm_code).first()

    @staticmethod
    def count_ncms() -> int:
        return NCM.objects.count()

    @staticmethod
    def list_ncms():
        ncms = NCM.objects.all()
        count = ncms.count()
        return {"count": count, "ncms": ncms}

    def get_ncm(self, ncm_id: uuid.UUID):
        if not (ncm := self.get_ncm_by_id(ncm_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "NCM não encontrado")

        return ncm

    def update_ncm(self, jwt: dict, ncm_id: uuid.UUID, payload: NCMSUpdateSchema):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        ncm = self.get_ncm(ncm_id)

        if payload.code is not None:
            ncm.code = payload.code

        if payload.group is not None:
            ncm_group = self.get_ncm_group(payload.group)
            ncm.group = ncm_group

        try:
            ncm.save()
        except IntegrityError as exc:
            raise HttpError(
                HTTPStatus.BAD_REQUEST, "NCM com o código especificado já existe"
            ) from exc

        return ncm

    def delete_ncm(self, jwt: dict, ncm_id: uuid.UUID):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.FORBIDDEN, "Usuário não autorizado")

        if self.count_ncms() <= 1:
            raise HttpError(
                HTTPStatus.BAD_REQUEST, "Não é possível deletar o último NCM"
            )

        ncm = self.get_ncm(ncm_id)
        ncm.delete()

        return JsonResponse(
            {"detail": "NCM deletado com sucesso"}, status=HTTPStatus.OK
        )
