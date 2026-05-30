from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import WatchHistory
from .serializers import UserSerializer, WatchHistorySerializer

User = get_user_model()


def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>StreamFolio</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                margin: 40px;
                background: #101827;
                color: white;
            }
            .card {
                max-width: 760px;
                padding: 30px;
                border-radius: 18px;
                background: #182235;
                box-shadow: 0 10px 30px rgba(0,0,0,.35);
            }
            a {
                color: #7dd3fc;
                display: block;
                margin: 12px 0;
                font-size: 18px;
            }
            .status {
                padding: 10px 14px;
                background: #064e3b;
                border-radius: 10px;
                display: inline-block;
                margin-bottom: 16px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="status">Backend Running</div>
            <h1>StreamFolio</h1>
            <p>Your streaming watch-history dashboard backend is live locally.</p>

            <h2>Quick Links</h2>
            <a href="/admin/">Django Admin</a>
            <a href="/api/users/">Users API</a>
            <a href="/api/watch-history/">Watch History API</a>

            <h2>What Works Now</h2>
            <p>You can create users, add watch-history records, and view them through the API.</p>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class WatchHistoryViewSet(viewsets.ModelViewSet):
    queryset = WatchHistory.objects.all().order_by('-watched_at')
    serializer_class = WatchHistorySerializer
    permission_classes = [AllowAny]
