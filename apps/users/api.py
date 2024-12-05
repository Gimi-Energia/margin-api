import uuid

from ninja import File, Router
from ninja.files import UploadedFile

from utils.jwt import JWTAuth, decode_jwt_token

from .schema import ChangePasswordSchema, UpdateUserSchema, UserCardSchema, UserSchema
from .service import UserService

user_router = Router(auth=JWTAuth())
service = UserService()


@user_router.get("/{user_id}", response=UserSchema)
def retrieve_user(request, user_id: uuid.UUID):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.get_user(user_id)


@user_router.patch("/{user_id}", response=UserSchema)
def update_user(request, user_id: uuid.UUID, payload: UpdateUserSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.update_user(user_id, payload)


@user_router.get("/{user_id}/cards", response=list[UserCardSchema])
def list_user_cards(request, user_id: uuid.UUID, search: str = None):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.list_user_cards(user_id=user_id, search=search)


@user_router.post("/add-card/{card_id}")
def add_card_to_users(request, card_id: int, department_id: int = None):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.add_card_to_users(card_id=card_id, department_id=department_id)


@user_router.post("/{user_id}/upload-picture", response=UserSchema)
def upload_picture(request, user_id: uuid.UUID, file: UploadedFile = File(...)):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.upload_user_picture(user_id, file)


@user_router.post("/{user_id}/change-password")
def change_password(request, user_id: uuid.UUID, payload: ChangePasswordSchema):
    decode_jwt_token(request.headers.get("Authorization"))
    return service.change_user_password(user_id, payload)
