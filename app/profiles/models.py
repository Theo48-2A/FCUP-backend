from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    """
    Modèle de profil utilisateur.
    Chaque utilisateur (`User`) possède un profil (`Profile`).
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profil de {self.user.username}"
