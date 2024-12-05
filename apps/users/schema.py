import uuid
from typing import Optional

from ninja import Schema


class CardSchema(Schema):
    id: int
    name: str
    link: Optional[str] = None


class UserCardSchema(Schema):
    card: CardSchema
    order: int


class DepartmentSchema(Schema):
    name: str


class UserSchema(Schema):
    id: uuid.UUID
    email: str
    name: str
    company: str
    department: DepartmentSchema
    type: str
    theme: str
    color: str
    picture: Optional[str] = None
    cards: list[UserCardSchema]


class UpdateUserSchema(Schema):
    color: Optional[str] = None
    theme: Optional[str] = None
    cards: Optional[list[int]] = None


class ChangePasswordSchema(Schema):
    new_password: str
    confirm_password: str
