from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken



class RegisterView(APIView):
    """
    Vue permettant l'inscription d'un utilisateur.
    """
    permission_classes = [AllowAny]  # Tout le monde peut accéder à cette vue.

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=201)  # Retourne les données de l'utilisateur créé.
        return Response(serializer.errors, status=400)  # Retourne les erreurs de validation.


class LogoutView(APIView):
    """
    Vue pour la déconnexion (ajoute le token de rafraîchissement à une liste noire).
    """
    permission_classes = [AllowAny]  # Autorise tout le monde à accéder au logout, pas besoin d'être authentifié

    def post(self, request):
        print("Début de la méthode POST de LogoutView")
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                print("Erreur : Aucun token de rafraîchissement fourni")
                return Response({"error": "Refresh token is required"}, status=400)

            token = RefreshToken(refresh_token)
            token.blacklist()
            print("Token ajouté à la liste noire avec succès")

            return Response(status=204)
        except Exception as e:
            print("Erreur lors du traitement :", str(e))
            return Response({"error": str(e)}, status=400)
