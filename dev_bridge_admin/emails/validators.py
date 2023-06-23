import magic

from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class MimeTypeValidator:
    """Валидатор для проверки MIME-типов в FileField"""

    mimetype_error_message = "Файлы формата {mimetype} не подходят для этого поля. " \
                             "Допустимы файлы {allowed_mimetypes}"
    unclear_type_error_message = "Не удалось определить тип файла {file}"

    def __init__(self, allowed_mimetypes: dict[str, str]):
        """Ключами в allowed_mimetypes выступает читаемое представление MIME-типа, значениями - сам MIME-type"""

        self.allowed_mimetypes = allowed_mimetypes

    def __call__(self, data):
        try:
            mime = magic.from_buffer(data.read(1024), mime=True)
            readable_mime = mime.split("/")[1]
            if mime not in self.allowed_mimetypes.values():
                raise ValidationError(self.mimetype_error_message.format(
                    mimetype=readable_mime,
                    allowed_mimetypes=", ".join(self.allowed_mimetypes.keys()),
                ))
        except AttributeError:
            raise ValidationError(self.unclear_type_error_message.format(file=data))

    def __eq__(self, other):
        return (
            isinstance(other, self.__class__) and
            self.allowed_mimetypes == other.allowed_mimetypes and
            self.mimetype_error_message == other.mimetype_error_message and
            self.unclear_type_error_message == other.unclear_type_error_message
        )
