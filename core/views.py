from rest_framework import viewsets
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
                max-width: 720px;
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
        </style>
    </head>
    <body>
        <div class="card">
            <h1>StreamFolio</h1>
            <p>Your streaming watch history dashboard is running.</p>

            <h2>Quick Links</h2>
            <a href="/admin/">Django Admin</a>
            <a href="/api/users/">Users API</a>
            <a href="/api/watch-history/">Watch History API</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WatchHistoryViewSet(viewsets.ModelViewSet):
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistorySerializer
