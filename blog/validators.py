from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible

@deconstructible
class NotOnlyNumbersValidator:
    def __init__(self, field_name="Este campo"):
        self.field_name = field_name

    def __call__(self, value, *args, **kwds):
        if value and value.isdigit():
            raise ValidationError(
                f"{self.field_name} no puede contener solo números."
            )