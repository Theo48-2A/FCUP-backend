from django.core.exceptions import ValidationError
import os

ALLOWED_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.webp']

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1].lower()  # Récupère l'extension du fichier
    if ext not in ALLOWED_EXTENSIONS:
        raise ValidationError(f"Format non supporté. Formats autorisés: {', '.join(ALLOWED_EXTENSIONS)}")
