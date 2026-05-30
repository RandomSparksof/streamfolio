import os
import requests
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import WatchHistory
from .serializers import UserSerializer, WatchHistorySerializer

User = get_user_model()

WATCHMODE_API_KEY = os.environ.get('WATCHMODE_API_KEY', '')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]


class WatchHistoryViewSet(viewsets.ModelViewSet):
    serializer_class = WatchHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return WatchHistory.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['post'], url_path='fetch')
    def fetch_from_watchmode(self, request):
        title_id = request.data.get('title_id')
        if not title_id:
            return Response({'error': 'title_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        url = f"https://api.watchmode.com/v1/title/{title_id}/sources/?apiKey={WATCHMODE_API_KEY}"
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return Response({'error': 'Watchmode API request failed'}, status=status.HTTP_502_BAD_GATEWAY)

        return Response(response.json())
