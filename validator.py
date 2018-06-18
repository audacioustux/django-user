from django.core.exceptions import ValidationError
from nobinalo.settings.local import Bad_Word
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


def validate_check_blacklist(value):
    if value in Bad_Word:
        raise ValidationError(
            _('\'%(value)s\' is listed as bad word. Please use another username.'),
            params={'value': value},
        )


validate_username_regex = RegexValidator(
    regex=r'^(?=.{3,}$)(?![_.])(?!.*[_.]{2})(?=.*[a-z])[a-z0-9._]+(?<![_.])$',
    # (?=.{3,30}$) = username is 3-30 characters long. (max_length value used in model)
    # (?![_.]) = no _ or . at the beginning
    # (?!.*[_.]{2}) = no __ or _. or ._ or .. inside
    # (?=.*[a-z]) = at least one alphabet
    # [a-z0-9._] = allowed characters
    # (?<![_.]) = no _ or . at the end
    # TODO: structured error massage
)
