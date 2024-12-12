import uuid
from http import HTTPStatus

from ninja.errors import HttpError

from apps.margin.models import Percentage
from apps.margin.schema import PercentageUpdateSchema


class PercentageService:
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
        self, percentage_id: uuid.UUID, payload: PercentageUpdateSchema
    ):
        if not (percentage := self.get_percentage_by_id(percentage_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Percentual não encontrado")

        for attr, value in payload.model_dump(
            exclude_defaults=True, exclude_unset=True
        ).items():
            setattr(percentage, attr, value)

        percentage.save()
        return percentage
