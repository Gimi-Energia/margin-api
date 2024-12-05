import os
import re
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import Optional

from django.db import transaction
from django.http import JsonResponse
from ninja import File
from ninja.errors import HttpError
from ninja.files import UploadedFile

from utils.validation import ValidationService

from .models import Card, CustomUser, Department, UserCard
from .schema import (
    CardSchema,
    ChangePasswordSchema,
    UpdateUserSchema,
    UserCardSchema,
    UserSchema,
)


class UserService:
    @property
    def card_service(self):
        return CardService()

    @property
    def department_service(self):
        return DepartmentService()

    @property
    def validation_service(self):
        return ValidationService()

    @staticmethod
    def build_user_response(user: CustomUser, user_cards):
        user_data = UserSchema(
            id=user.id,
            email=user.email,
            name=user.name,
            company=user.company,
            department=user.department,
            type=user.type,
            theme=user.theme,
            color=user.color,
            picture=user.picture,
            cards=[
                UserCardSchema(
                    card=CardSchema(
                        id=user_card.card.id,
                        name=user_card.card.name,
                        link=user_card.card.link,
                    ),
                    order=user_card.order,
                )
                for user_card in user_cards
            ],
        )

        return user_data

    @staticmethod
    def validate_password(password: str) -> bool:
        if len(password) < 8:
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[@$!%*?&#]", password):
            return False
        return True

    def get_user_by_id(self, user_id: uuid.UUID) -> CustomUser:
        return CustomUser.objects.get(pk=user_id)

    def get_user_cards(self, user: CustomUser) -> list[CustomUser]:
        return (
            UserCard.objects.filter(user=user).select_related("card").order_by("order")
        )

    def get_user(self, user_id: uuid.UUID) -> UserSchema:
        if not (user := self.get_user_by_id(user_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

        user_cards = self.get_user_cards(user=user)
        user_data = self.build_user_response(user=user, user_cards=user_cards)

        return user_data

    def update_user(self, user_id: uuid.UUID, payload: UpdateUserSchema) -> CustomUser:
        if not (user := self.get_user_by_id(user_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

        with transaction.atomic():
            if payload.cards:
                self._handle_card_updates(user, payload.cards)
            else:
                self._update_user_fields(user, payload)

            user.save()
            user.refresh_from_db()

            user_cards = self.get_user_cards(user=user)
            user_data = self.build_user_response(user=user, user_cards=user_cards)

        return user_data

    def _update_user_fields(self, user: CustomUser, payload: UpdateUserSchema) -> None:
        if payload.color:
            user.color = payload.color

        if payload.theme:
            user.theme = payload.theme

    def _handle_card_updates(self, user: CustomUser, cards: list[int]) -> None:
        if cards is None:
            return

        card_count = self.card_service.count_user_cards(user.id)
        if len(cards) != card_count:
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                f"Esperado {card_count} cards, mas recebeu {len(cards)}. Tente novamente sem filtros.",
            )

        self.card_service.delete_all_user_cards(user_id=user.id)
        for index, card_id in enumerate(cards):
            if not (card := self.card_service.get_card_by_id(card_id)):
                raise HttpError(HTTPStatus.NOT_FOUND, "Card não encontrado")

            UserCard.objects.create(user=user, card=card, order=index + 1)

    def add_card_to_users(
        self, card_id: uuid.UUID, department_id: Optional[int] = None
    ) -> JsonResponse:
        if not (card := self.card_service.get_card_by_id(card_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Card não encontrado")

        if department_id is not None:
            if not (
                department := self.department_service.get_department_by_id(
                    department_id
                )
            ):
                raise HttpError(HTTPStatus.NOT_FOUND, "Departamento não encontrado")
            users = CustomUser.objects.filter(department=department)
            if not users.exists():
                raise HttpError(
                    HTTPStatus.NOT_FOUND, "Nenhum usuário encontrado nesse departamento"
                )
        else:
            users = CustomUser.objects.all()

        with transaction.atomic():
            for user in users:
                if not UserCard.objects.filter(user=user, card=card).exists():
                    order = self.card_service.count_user_cards(user_id=user.id) + 1
                    UserCard.objects.create(user=user, card=card, order=order)

        return JsonResponse(
            {"success": "Card adicionado para os usuários"}, status=HTTPStatus.OK
        )

    def upload_user_picture(
        self, user_id: uuid.UUID, file: UploadedFile = File(...)
    ) -> CustomUser:
        if not (user := self.get_user_by_id(user_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

        self._validate_image(file)

        file.name = self._generate_new_filename(user_id, file.name)

        user.picture = file
        user.save()
        user.refresh_from_db()

        user_cards = self.get_user_cards(user=user)
        user_data = self.build_user_response(user=user, user_cards=user_cards)

        return user_data

    def _validate_image(self, file: UploadedFile) -> None:
        if not self.validation_service.validate_image_format(file.name):
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                "Tipos permitidos: jpg, jpeg e png",
            )
        if not self.validation_service.validate_image_size(file):
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                f"A imagem excede o limite de {self.validation_service.MAX_IMAGE_SIZE_MB} MB",
            )

    def _generate_new_filename(self, user_id: uuid.UUID, original_filename: str) -> str:
        file_extension = os.path.splitext(original_filename)[1]
        timestamp = datetime.now().strftime("%d_%m_%y_%H_%M_%S")
        return f"{user_id}_{timestamp}{file_extension}"

    def change_user_password(
        self, user_id: uuid.UUID, payload: ChangePasswordSchema
    ) -> JsonResponse:
        if not (user := self.get_user_by_id(user_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

        self._validate_passwords(payload)

        user.set_password(payload.new_password)
        user.save()

        return JsonResponse(
            {"success": "Senha alterada com sucesso"}, status=HTTPStatus.OK
        )

    def _validate_passwords(self, payload: ChangePasswordSchema) -> None:
        if payload.new_password != payload.confirm_password:
            raise HttpError(HTTPStatus.BAD_REQUEST, "As senhas não coincidem")

        if not self.validate_password(payload.new_password):
            raise HttpError(
                HTTPStatus.BAD_REQUEST,
                "A nova senha deve ter pelo menos 8 caracteres, incluindo letras maiúsculas, minúsculas, números e símbolos.",
            )

    def list_user_cards(
        self, user_id: uuid.UUID, search: Optional[str] = None
    ) -> list[UserCard]:
        if not (user := self.get_user_by_id(user_id)):
            raise HttpError(HTTPStatus.NOT_FOUND, "Usuário não encontrado")

        user_cards = UserCard.objects.filter(user=user).select_related("card")
        if search:
            user_cards = user_cards.filter(card__name__icontains=search)
        return user_cards.order_by("order")


class CardService:
    def count_cards(self) -> int:
        return Card.objects.count()

    def count_user_cards(self, user_id: uuid.UUID) -> int:
        return UserCard.objects.filter(user_id=user_id).count()

    def get_card_by_id(self, card_id: uuid.UUID) -> Card:
        return Card.objects.get(pk=card_id)

    def delete_all_user_cards(self, user_id: uuid.UUID) -> None:
        UserCard.objects.filter(user=user_id).delete()


class DepartmentService:
    def get_department_by_id(self, department_id: uuid.UUID) -> Department:
        return Department.objects.get(pk=department_id)
