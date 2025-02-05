from django.urls import path
from .views import ProfileDetailView, PublicProfileView

urlpatterns = [
    path('me/', ProfileDetailView.as_view(), name='my-profile'),  # Récupération & mise à jour du profil
    path('<str:user__username>/', PublicProfileView.as_view(), name='public-profile'),  # Profil public
]
