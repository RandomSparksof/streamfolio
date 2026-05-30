from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import WatchHistory

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class WatchHistorySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = WatchHistory
        fields = [
            'id',
            'user',
            'username',
            'title',
            'service_name',
            'watched_at',
            'content_type',
            'reaction',
            'rating',
            'notes',
        ]
