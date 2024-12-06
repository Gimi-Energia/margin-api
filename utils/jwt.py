from http import HTTPStatus

from jose import ExpiredSignatureError, jwt
from ninja.errors import HttpError
from ninja.security import HttpBearer

from core import settings


class JWTAuth(HttpBearer):
    def authenticate(self, request, token: str) -> bool:
        try:
            user = jwt.decode(token, settings.SECRET_KEY)
            request.user = user
            return True
        except ExpiredSignatureError as exception:
            raise HttpError(HTTPStatus.UNAUTHORIZED, str(exception)) from exception
        except Exception:  # pylint: disable=broad-exception-caught
            return False


def decode_jwt_token(token: str):
    secret_key = settings.SECRET_KEY
    if "Bearer" in token:
        token = token.split(" ")[1]
    return jwt.decode(token, secret_key, algorithms=["HS256"])
