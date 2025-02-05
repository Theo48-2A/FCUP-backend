from rest_framework import serializers
from django.conf import settings
from .models import Profile
from django.contrib.auth.models import User


class ProfileSerializer(serializers.ModelSerializer):
    """Serializer pour récupérer les informations complètes du profil personnel"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'avatar', 'bio', 'phone', 'birth_date']

    def get_avatar(self, obj):
        """Retourne l'URL complète de l'avatar"""
        request = self.context.get('request')

        if obj.avatar:
            avatar_url = obj.avatar.url
        else:
            avatar_url = settings.MEDIA_URL + 'avatars/default.jpg'

        if request:
            return request.build_absolute_uri(avatar_url)
        return avatar_url


class PublicProfileSerializer(serializers.ModelSerializer):
    """Serializer pour afficher le profil d'autres utilisateurs (profil public)"""
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'username', 'avatar', 'bio']

    def get_avatar(self, obj):
        """Retourne l'URL complète de l'avatar"""
        request = self.context.get('request')

        if obj.avatar:
            avatar_url = obj.avatar.url
        else:
            avatar_url = settings.MEDIA_URL + 'avatars/default.jpg'

        if request:
            return request.build_absolute_uri(avatar_url)
        return avatar_url


class ProfileUpdateSerializer(serializers.ModelSerializer):
    """Serializer pour mettre à jour uniquement les champs modifiables du profil"""
    username = serializers.CharField(source='user.username', read_only=True)  # Empêche la modification
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'username', 'email', 'avatar', 'bio', 'phone', 'birth_date']

    def update(self, instance, validated_data):
        """
        Permet de gérer la suppression d'un avatar (si l'utilisateur met `null`).
        """
        if 'avatar' in validated_data and validated_data['avatar'] is None:
            instance.avatar.delete(save=False)  # Supprime l'ancien fichier
            instance.avatar = None

        return super().update(instance, validated_data)
