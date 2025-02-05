from rest_framework import generics, permissions
from .models import Profile
from .serializers import ProfileSerializer, ProfileUpdateSerializer, PublicProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Vue permettant de récupérer et modifier son propre profil.
    - ✅ Retourne `username`, `email`, `bio`, `phone`, `birth_date`
    - ✅ Utilise `ProfileUpdateSerializer` pour empêcher la modification de `username` et `email`
    """
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  # Récupère le profil de l'utilisateur connecté


class PublicProfileView(generics.RetrieveAPIView):
    """
    Vue pour afficher un profil public. Pas besoin d'authentification.
    - ✅ Retourne `username`, `avatar`, `bio` (infos publiques uniquement)
    - ✅ Recherche via `user.id`
    """
    queryset = Profile.objects.all()
    serializer_class = PublicProfileSerializer
    permission_classes = [permissions.AllowAny]  # Accès public
    lookup_field = "user__id"  # Recherche du profil par `user.id` au lieu de `username`
