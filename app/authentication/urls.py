from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import CustomTokenRefreshView
from .views import RegisterView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),  # Inscription
    path('login/', TokenObtainPairView.as_view(), name='login'),  # Connexion
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Déconnexion
]
