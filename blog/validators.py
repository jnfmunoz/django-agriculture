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
        
@deconstructible
class MinMaxLengthValidator:
    def __init__(self, min_length=None, max_length=None, field_name="Este campo"):
        self.min_length = min_length
        self.max_length = max_length
        self.field_name = field_name

    def __call__(self, value, *args, **kwds):
        if value is None:
            return
        
        length = len(value)
    
        if self.min_length is not None and length < self.min_length:
            raise ValidationError(
                f"{self.field_name} debe tener al menos {self.min_length} caracteres."
            )    
        
        if self.max_length is not None and length > self.max_length:
            raise ValidationError(
                f"{self.field_name} no puede superar los {self.max_length} caracteres."
            )

@deconstructible
class NotEmptyValidator:
    def __init__(self, field_name="Este campo"):
        self.field_name = field_name

    def __call__(self, value, *args, **kwds):
        if value is None:
            raise ValidationError(f"{self.field_name} no puede estar vacío.")
        
        if isinstance(value, str) and not value.strip():
            raise ValidationError(f"{self.field_name} no puede estar vacío.")
        