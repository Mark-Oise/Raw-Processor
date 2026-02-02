import os
from django.core.exceptions import ValidationError


def validate_raw_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.nef', '.cr2', '.arw', '.dng']
    if ext not in valid_extensions:
        raise ValidationError(f"Unsupported file. Allowed: {valid_extensions}")
