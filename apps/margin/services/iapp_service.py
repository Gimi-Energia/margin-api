from http import HTTPStatus

import requests
from ninja.errors import HttpError


class IappService:
    BASE_URL = "https://api.iniciativaaplicativos.com.br"

    def get(self, endpoint: str, params: dict, token: str, secret: str):
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"TOKEN": token, "SECRET": secret}
        response = requests.get(url, params=params, headers=headers, timeout=10)

        if response.ok:
            response_data = response.json()
            if response_data.get("success") is False:
                raise HttpError(HTTPStatus.BAD_REQUEST, response_data.get("message"))
            return response_data

        raise HttpError(
            HTTPStatus.FAILED_DEPENDENCY,
            f"Erro {response.status_code}: Instabilidade no iApp.",
        )

    def put(self, endpoint: str, payload: dict, token: str, secret: str):
        url = f"{self.BASE_URL}{endpoint}"
        headers = {"TOKEN": token, "SECRET": secret}
        response = requests.put(url, json=payload, headers=headers, timeout=10)

        if response.ok:
            response_data = response.json()
            if response_data.get("success") is False:
                raise HttpError(HTTPStatus.BAD_REQUEST, response_data.get("message"))
            return response_data

        raise HttpError(
            HTTPStatus.FAILED_DEPENDENCY,
            f"Erro {response.status_code}: Instabilidade no iApp.",
        )
