import uuid
from http import HTTPStatus

from ninja.errors import HttpError

from apps.margin.models import Percentage
from apps.margin.schema import PercentageUpdateSchema
from utils.validation import ValidationService


class PercentageService:
    def __init__(self):
        self.validation_service = ValidationService()

    @staticmethod
    def get_percentage_by_id(percentage_id: uuid.UUID):
        return Percentage.objects.filter(pk=percentage_id).first()

    @staticmethod
    def list_percentages():
        percentages = Percentage.objects.all()
        count = percentages.count()

        return {
            "count": count,
            "percentages": percentages,
        }

    def get_percentage(self, percentage_id: uuid.UUID):
        if not (percentage := self.get_percentage_by_id(percentage_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Percentual não encontrado")

        return percentage

    def update_percentage(
        self, jwt: dict, percentage_id: uuid.UUID, payload: PercentageUpdateSchema
    ):
        if not self.validation_service.validate_user_access(jwt):
            raise HttpError(HTTPStatus.UNAUTHORIZED, "Usuário não autorizado")

        percentage = self.get_percentage(percentage_id)

        for attr, value in payload.model_dump(
            exclude_defaults=True, exclude_unset=True
        ).items():
            setattr(percentage, attr, value)

        percentage.save()
        return percentage
