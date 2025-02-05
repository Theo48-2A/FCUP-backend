from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.conf import settings
from .validators import validate_image_extension
import os


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    avatar = models.ImageField(
        upload_to='avatars/',  # Sauvegarde sous /media/avatars/
        storage=default_storage,  # Assure que le stockage suit MEDIA_ROOT
        blank=True,
        null=True,
        default='avatars/default.jpg',  # Image par défaut sous /media/avatars/
        validators=[validate_image_extension],
        max_length=255  # Bonne pratique
    )

    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def get_avatar_url(self):
        """
        Retourne l'URL absolue de l'avatar.
        - Si l'utilisateur a un avatar personnalisé, retourne son URL.
        - Sinon, retourne l'URL du fichier `default.jpg`.
        """
        if self.avatar:
            return f"{settings.MEDIA_URL}{self.avatar}"
        return f"{settings.MEDIA_URL}avatars/default.jpg"

    def __str__(self):
        return f"Profile of {self.user.username}"
