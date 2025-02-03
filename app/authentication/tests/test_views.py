import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

@pytest.fixture
def api_client():
    """Fixture pour un client de l'API DRF."""
    return APIClient()

@pytest.mark.django_db
def test_register_success(api_client):
    """
    Test d’inscription réussi.
    """
    url = reverse('register')  # correspond à name='register' dans urls.py
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'mypassword123'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert 'id' in response.data
    assert response.data['username'] == 'newuser'
    # Vérifie en base si l'utilisateur a bien été créé
    user = User.objects.get(username='newuser')
    assert user.email == 'newuser@example.com'
    assert user.check_password('mypassword123')

@pytest.mark.django_db
def test_register_missing_fields(api_client):
    """
    Test d’inscription échoué à cause de champs manquants.
    """
    url = reverse('register')
    data = {
        'username': '',  # ou on ne met pas l'email
        'email': 'missing@example.com',
        'password': 'testpass'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 400
    assert 'username' in response.data  # on s’attend à avoir une erreur sur le champ manquant

@pytest.mark.django_db
def test_login_success(api_client):
    """
    Test de connexion qui devrait réussir.
    """
    # On créé d'abord un user en base
    user = User.objects.create_user(username='loginuser', password='testpass')
    url = reverse('login')  # name='login' => TokenObtainPairView
    data = {
        'username': 'loginuser',
        'password': 'testpass'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

@pytest.mark.django_db
def test_login_failure(api_client):
    """
    Test de connexion échoué (mauvais mot de passe).
    """
    user = User.objects.create_user(username='loginuser2', password='rightpassword')
    url = reverse('login')
    data = {
        'username': 'loginuser2',
        'password': 'wrongpassword'
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 401
    # Vérifiez la structure ou le message d’erreur si nécessaire
    assert 'access' not in response.data

@pytest.mark.django_db
def test_logout(api_client):
    """
    Test du logout : on blacklist le refresh token et on doit avoir un code 204.
    """
    # On créé un user + on obtient un refresh token en se loguant
    user = User.objects.create_user(username='logoutuser', password='testpass')
    login_url = reverse('login')
    logout_url = reverse('logout')

    # On récupère access + refresh en simulant le login
    login_data = {
        'username': 'logoutuser',
        'password': 'testpass'
    }
    login_response = api_client.post(login_url, login_data, format='json')
    refresh_token = login_response.data['refresh']

    # Appel au logout
    response = api_client.post(logout_url, {'refresh': refresh_token}, format='json')
    assert response.status_code == 204

@pytest.mark.django_db
def test_custom_token_refresh(api_client):
    """
    Test de la vue CustomTokenRefreshView, qui doit renvoyer un nouveau token
    et blacklister l'ancien.
    """
    # Création d'un user et obtention d'un token (pour simuler un refresh en cours)
    user = User.objects.create_user(username='refreshuser', password='testpass')
    refresh_token = RefreshToken.for_user(user)  # Génère un refresh pour l'user

    # On appelle la vue custom /token/refresh/ avec l'ancien refresh token
    url = reverse('token_refresh')  # name='token_refresh'
    data = {
        'refresh': str(refresh_token),
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 200
    assert 'access' in response.data
    # Normalement, la vue renvoie un "refresh" mis à jour
    assert 'refresh' in response.data
    new_refresh = response.data['refresh']
    assert new_refresh != str(refresh_token)  # On veut un nouveau token

    # Vérifier que l'ancien token est black-listé
    # Tenter de le réutiliser, on doit avoir une erreur de token invalidé.
    invalid_response = api_client.post(url, {'refresh': str(refresh_token)}, format='json')
    assert invalid_response.status_code == 401 or invalid_response.status_code == 400
