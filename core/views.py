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
        content_type = request.POST.get("content_type", "other")
        reaction = request.POST.get("reaction", "neutral")
        rating = request.POST.get("rating")
        notes = request.POST.get("notes", "")

        if title and service_name and user_id:
            user = User.objects.get(id=user_id)

            rating_value = None
            if rating:
                try:
                    rating_value = int(rating)
                except ValueError:
                    rating_value = None

            WatchHistory.objects.create(
                user=user,
                title=title,
                service_name=service_name,
                content_type=content_type,
                reaction=reaction,
                rating=rating_value,
                notes=notes,
                watched_at=timezone.now()
            )

        return redirect("/")

    search_query = request.GET.get("search", "").strip()
    service_filter = request.GET.get("service", "").strip()
    reaction_filter = request.GET.get("reaction", "").strip()

    watch_items = WatchHistory.objects.all().order_by("-watched_at")

    if search_query:
        watch_items = watch_items.filter(title__icontains=search_query)

    if service_filter:
        watch_items = watch_items.filter(service_name__icontains=service_filter)

    if reaction_filter:
        watch_items = watch_items.filter(reaction=reaction_filter)

    total_items = WatchHistory.objects.count()
    liked_count = WatchHistory.objects.filter(reaction="liked").count()
    disliked_count = WatchHistory.objects.filter(reaction="disliked").count()
    neutral_count = WatchHistory.objects.filter(reaction="neutral").count()

    average_rating = 0
    rated_items = WatchHistory.objects.exclude(rating__isnull=True)

    if rated_items.exists():
        total_rating = sum(item.rating for item in rated_items if item.rating)
        average_rating = round(total_rating / rated_items.count(), 1)

    displayed_items = watch_items[:50]

    user_options = ""

    for user in users:
        user_options += f"""
        <option value="{user.id}">{user.username}</option>
        """

    rows = ""

    for item in displayed_items:
        rating_display = item.rating if item.rating else ""
        notes_display = item.notes if item.notes else ""

        rows += f"""
        <tr>
            <td>{item.title}</td>
            <td>{item.service_name}</td>
            <td>{item.content_type.title()}</td>
            <td>{item.reaction.title()}</td>
            <td>{rating_display}</td>
            <td>{item.watched_at.strftime('%Y-%m-%d %I:%M %p')}</td>
            <td>{item.user.username}</td>
            <td>{notes_display}</td>
        </tr>
        """

    if not rows:
        rows = """
        <tr>
            <td colspan="8" class="empty">No matching watch history found.</td>
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
                max-width: 1280px;
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
                font-size: 46px;
                margin: 0 0 10px;
            }}

            h2 {{
                margin-top: 0;
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

            .stats {{
                display: grid;
                grid-template-columns: repeat(5, minmax(0, 1fr));
                gap: 16px;
                margin-bottom: 24px;
            }}

            .stat {{
                background: #182235;
                border-radius: 18px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0,0,0,.22);
            }}

            .stat .number {{
                font-size: 30px;
                font-weight: bold;
                margin-bottom: 6px;
                color: #7dd3fc;
            }}

            .stat .label {{
                color: #cbd5e1;
                font-size: 14px;
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
                overflow-x: auto;
            }}

            .form-grid {{
                display: grid;
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 16px;
            }}

            .filter-grid {{
                display: grid;
                grid-template-columns: 2fr 1fr 1fr auto;
                gap: 12px;
                align-items: end;
            }}

            label {{
                display: block;
                margin-bottom: 8px;
                color: #93c5fd;
                font-weight: bold;
            }}

            input, select, textarea {{
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

            textarea {{
                min-height: 90px;
                resize: vertical;
            }}

            .full {{
                grid-column: 1 / -1;
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

            .secondary-link {{
                color: #7dd3fc;
                text-decoration: none;
                display: inline-block;
                margin-left: 10px;
                font-weight: bold;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 16px;
                min-width: 1100px;
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
                vertical-align: top;
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

            @media (max-width: 900px) {{
                .stats {{
                    grid-template-columns: repeat(2, minmax(0, 1fr));
                }}

                .form-grid, .filter-grid {{
                    grid-template-columns: 1fr;
                }}

                h1 {{
                    font-size: 34px;
                }}
            }}
        </style>
    </head>
    <body>
        <div class="page">
            <div class="hero">
                <div class="status">Backend Running</div>
                <h1>StreamFolio</h1>
                <p>Your personal streaming history dashboard. Track what you watched, where you watched it, what you thought, and what you want to recommend later.</p>

                <div class="links">
                    <a href="/admin/">Django Admin</a>
                    <a href="/api/users/">Users API</a>
                    <a href="/api/watch-history/">Watch History API</a>
                </div>
            </div>

            <div class="stats">
                <div class="stat">
                    <div class="number">{total_items}</div>
                    <div class="label">Total Items</div>
                </div>
                <div class="stat">
                    <div class="number">{liked_count}</div>
                    <div class="label">Liked</div>
                </div>
                <div class="stat">
                    <div class="number">{neutral_count}</div>
                    <div class="label">Neutral</div>
                </div>
                <div class="stat">
                    <div class="number">{disliked_count}</div>
                    <div class="label">Disliked</div>
                </div>
                <div class="stat">
                    <div class="number">{average_rating}</div>
                    <div class="label">Average Rating</div>
                </div>
            </div>

            <div class="grid">
                <div class="card">
                    <h2>Add Watch Item</h2>

                    <form method="post">
                        <div class="form-grid">
                            <div>
                                <label>Title</label>
                                <input type="text" name="title" placeholder="Example: The Bear" required>
                            </div>

                            <div>
                                <label>Streaming Service</label>
                                <input type="text" name="service_name" placeholder="Example: Hulu" required>
                            </div>

                            <div>
                                <label>User</label>
                                <select name="user_id" required>
                                    {user_options}
                                </select>
                            </div>

                            <div>
                                <label>Content Type</label>
                                <select name="content_type">
                                    <option value="movie">Movie</option>
                                    <option value="show">Show</option>
                                    <option value="episode">Episode</option>
                                    <option value="documentary">Documentary</option>
                                    <option value="standup">Standup</option>
                                    <option value="other" selected>Other</option>
                                </select>
                            </div>

                            <div>
                                <label>Reaction</label>
                                <select name="reaction">
                                    <option value="liked">Liked</option>
                                    <option value="neutral" selected>Neutral</option>
                                    <option value="disliked">Disliked</option>
                                </select>
                            </div>

                            <div>
                                <label>Rating 1-10</label>
                                <input type="number" name="rating" min="1" max="10" placeholder="Example: 9">
                            </div>

                            <div class="full">
                                <label>Notes</label>
                                <textarea name="notes" placeholder="Example: Great acting, chaotic kitchen energy, worth recommending."></textarea>
                            </div>
                        </div>

                        <button type="submit">Add to Watch History</button>
                    </form>
                </div>

                <div class="card">
                    <h2>Search & Filter</h2>

                    <form method="get">
                        <div class="filter-grid">
                            <div>
                                <label>Search Title</label>
                                <input type="text" name="search" value="{search_query}" placeholder="Search by title">
                            </div>

                            <div>
                                <label>Service</label>
                                <input type="text" name="service" value="{service_filter}" placeholder="Hulu, Netflix, Max">
                            </div>

                            <div>
                                <label>Reaction</label>
                                <select name="reaction">
                                    <option value="">All</option>
                                    <option value="liked">Liked</option>
                                    <option value="neutral">Neutral</option>
                                    <option value="disliked">Disliked</option>
                                </select>
                            </div>

                            <div>
                                <button type="submit">Filter</button>
                                <a class="secondary-link" href="/">Reset</a>
                            </div>
                        </div>
                    </form>
                </div>

                <div class="card">
                    <h2>Recent Watch History</h2>
                    <table>
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Service</th>
                                <th>Type</th>
                                <th>Reaction</th>
                                <th>Rating</th>
                                <th>Watched At</th>
                                <th>User</th>
                                <th>Notes</th>
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
