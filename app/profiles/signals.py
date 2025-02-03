from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()  # Récupère le modèle User

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal qui écoute la création d'un utilisateur.
    À chaque création d'un utilisateur, on génère un profil associé.
    """
    if created:
        Profile.objects.create(user=instance)
