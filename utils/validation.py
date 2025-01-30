import re

from ninja.files import UploadedFile


class ValidationService:
    MAX_IMAGE_SIZE_MB = 4

    def validate_image_format(self, picture: str) -> bool:
        allowed_formats = ["jpg", "jpeg", "png"]
        return picture.split(".")[-1].lower() in allowed_formats

    def validate_image_size(self, file: UploadedFile) -> bool:
        max_size_in_bytes = self.MAX_IMAGE_SIZE_MB * 1024 * 1024
        if file.size > max_size_in_bytes:
            return False
        return True

    def validate_user_access(self, jwt_data) -> bool:
        return jwt_data.get("is_margin_admin", False) is True

    def validate_ncm_code_format(self, code: str) -> bool:
        return bool(re.match(r"^\d{4}\.\d{2}\.\d{2}$", code))
