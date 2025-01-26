from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # On expose uniquement ces champs


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']  # Champs à valider et enregistrer
        extra_kwargs = {
            'password': {'write_only': True},  # Le mot de passe ne sera pas exposé
        }

    def create(self, validated_data):
        """
        Crée un utilisateur en utilisant create_user() qui crypte le mot de passe.
        """
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
