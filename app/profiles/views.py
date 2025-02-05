from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    Vue permettant de récupérer et modifier son propre profil.
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  # Retourne le profil de l'utilisateur connecté
