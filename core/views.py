from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils import timezone
from .models import WatchHistory
from .serializers import UserSerializer, WatchHistorySerializer

User = get_user_model()


def home(request):
    users = User.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        service_name = request.POST.get("service_name")
        user_id = request.POST.get("user_id")

        if title and service_name and user_id:
            user = User.objects.get(id=user_id)

            WatchHistory.objects.create(
                user=user,
                title=title,
                service_name=service_name,
                watched_at=timezone.now()
            )

        return redirect("/")

    watch_items = WatchHistory.objects.all().order_by("-watched_at")[:25]

    user_options = ""

    for user in users:
        user_options += f"""
        <option value="{user.id}">{user.username}</option>
        """

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
            <td colspan="4" class="empty">No watch history added yet.</td>
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

            .grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 24px;
            }}

            .card {{
                background: #182235;
                border-radius: 20px;
                padding: 26px;
                box-shadow: 0 10px 30px rgba(0,0,0,.28);
            }}

            label {{
                display: block;
                margin-bottom: 8px;
                color: #93c5fd;
                font-weight: bold;
            }}

            input, select {{
                width: 100%;
                padding: 12px;
                border-radius: 10px;
                border: 1px solid #334155;
                background: #0f172a;
                color: white;
                margin-bottom: 16px;
                box-sizing: border-box;
                font-size: 16px;
            }}

            button {{
                background: #7dd3fc;
                color: #082f49;
                border: none;
                padding: 13px 18px;
                border-radius: 12px;
                font-weight: bold;
                font-size: 16px;
                cursor: pointer;
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

            <div class="grid">
                <div class="card">
                    <h2>Add Watch Item</h2>

                    <form method="post">
                        <label>Title</label>
                        <input type="text" name="title" placeholder="Example: The Bear" required>

                        <label>Streaming Service</label>
                        <input type="text" name="service_name" placeholder="Example: Hulu" required>

                        <label>User</label>
                        <select name="user_id" required>
                            {user_options}
                        </select>

                        <button type="submit">Add to Watch History</button>
                    </form>
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
    queryset = WatchHistory.objects.all().order_by("-watched_at")
    serializer_class = WatchHistorySerializer
    permission_classes = [AllowAny]
