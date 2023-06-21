import re

from django.core.exceptions import ValidationError


def validate_username(value):
    if value.lower() == "me":
        raise ValidationError(
            ("Имя пользователя не может быть <me>."),
            params={"value": value},
        )
    if re.match(r"^[\w.@+-]+\Z", value) is None:
        raise ValidationError(
            ("Username содержит недопустимые символы "),
            params={"value": value},
        )
