from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.models import User



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



class CustomTokenRefreshView(TokenRefreshView):
    """
    Vue personnalisée pour retourner un nouveau access token et un nouveau refresh token,
    tout en révoquant le précédent refresh token.
    """
    def post(self, request, *args, **kwargs):
        # Validation : s'assurer que le refresh token est présent
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token is required"}, status=400)

        # Appel à la méthode parent pour générer le nouveau access token
        response = super().post(request, *args, **kwargs)

        # Si la réponse est un succès (200 OK), générer un nouveau refresh token
        if response.status_code == 200:
            try:
                # Extraire le payload du refresh token
                token = RefreshToken(refresh_token)
                user_id = token.payload.get("user_id")  # Récupérer l'ID utilisateur

                if not user_id:
                    raise AuthenticationFailed("Invalid token: no user_id found.")

                # Révoquer le refresh token précédent en le blacklistant
                token.blacklist()  # Ajoute le token à la blacklist

                # Récupérer l'utilisateur depuis la base de données
                user = User.objects.get(id=user_id)

                # Générer un nouveau refresh token pour cet utilisateur
                new_refresh_token = RefreshToken.for_user(user)
                response.data["refresh"] = str(new_refresh_token)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
            except Exception as e:
                return Response({"error": str(e)}, status=400)

        return response
