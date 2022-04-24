from django.core import validators as dj_validators


class AlphanumericHyphenValidator(dj_validators.RegexValidator):
    regex = r"^[a-z\d-]+\Z"
    message = "Invalid value. Should include only lowercase letters, numbers, and -"
    flags = 0


class HyphenOnlyValidator(dj_validators.RegexValidator):
    regex = r"^[-]*$"
    message = "Invalid value. Cannot be just hyphens."
    inverse_match = True
    flags = 0
