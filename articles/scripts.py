from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def is_string_an_url(url_string: str) -> bool:
    validate_url = URLValidator()
    try:
        validate_url(url_string)
    except ValidationError as e:
        return False
    return True
