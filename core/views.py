from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from .models import WatchHistory
from .serializers import UserSerializer, WatchHistorySerializer

User = get_user_model()


def home(request):
    watch_items = WatchHistory.objects.all().order_by('-watched_at')[:25]

    rows = ""

    for item in watch_items:
        rows += f"""
        <tr>
            <td>{item.title}</td>
            <td>{item.service_name}</td>
            <td>{item.watched_at.strftime('%Y-%m-%d %I:%M %p')}</td>
            <td>{item.user.username}</td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="4" class="empty">No watch history added yet. Add one in Django Admin.</td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>StreamFolio Dashboard</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                background: #0f172a;
                color: white;
            }}

            .page {{
                max-width: 1100px;
                margin: 0 auto;
                padding: 40px 24px;
            }}

            .hero {{
                background: linear-gradient(135deg, #1e293b, #111827);
                border-radius: 24px;
                padding: 36px;
                box-shadow: 0 16px 40px rgba(0,0,0,.35);
                margin-bottom: 28px;
            }}

            .status {{
                display: inline-block;
                background: #064e3b;
                color: #bbf7d0;
                padding: 8px 14px;
                border-radius: 999px;
                font-size: 14px;
                margin-bottom: 14px;
            }}

            h1 {{
                font-size: 44px;
                margin: 0 0 10px;
            }}

            p {{
                color: #cbd5e1;
                font-size: 18px;
            }}

            .links {{
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
                margin-top: 24px;
            }}

            .links a {{
                color: #082f49;
                background: #7dd3fc;
                text-decoration: none;
                padding: 12px 16px;
                border-radius: 12px;
                font-weight: bold;
            }}

            .card {{
                background: #182235;
                border-radius: 20px;
                padding: 26px;
                box-shadow: 0 10px 30px rgba(0,0,0,.28);
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 16px;
            }}

            th {{
                text-align: left;
                color: #93c5fd;
                border-bottom: 1px solid #334155;
                padding: 12px;
            }}

            td {{
                border-bottom: 1px solid #263244;
                padding: 12px;
                color: #e5e7eb;
            }}

            .empty {{
                text-align: center;
                color: #94a3b8;
                padding: 24px;
            }}

            .footer {{
                margin-top: 28px;
                color: #94a3b8;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="hero">
                <div class="status">Backend Running</div>
                <h1>StreamFolio</h1>
                <p>Your streaming watch-history dashboard is live locally.</p>

                <div class="links">
                    <a href="/admin/">Django Admin</a>
                    <a href="/api/users/">Users API</a>
                    <a href="/api/watch-history/">Watch History API</a>
                </div>
            </div>

            <div class="card">
                <h2>Recent Watch History</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Title</th>
                            <th>Service</th>
                            <th>Watched At</th>
                            <th>User</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>
            </div>

            <div class="footer">
                StreamFolio local development dashboard.
            </div>
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
