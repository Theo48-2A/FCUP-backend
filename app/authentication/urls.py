from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Inscription
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Connexion
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # Actualisation
    path('logout/', LogoutView.as_view(), name='logout'),  # Déconnexion
]
