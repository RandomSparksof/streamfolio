from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import redirect, get_object_or_404
from django.utils import timezone
from .models import WatchHistory
from .serializers import UserSerializer, WatchHistorySerializer

User = get_user_model()


def home(request):
    users = User.objects.all()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "delete":
            item_id = request.POST.get("item_id")
            item = get_object_or_404(WatchHistory, id=item_id)
            item.delete()
            return redirect("/")

        title = request.POST.get("title")
        service_name = request.POST.get("service_name")
        user_id = request.POST.get("user_id")
        content_type = request.POST.get("content_type", "other")
        reaction = request.POST.get("reaction", "neutral")
        rating = request.POST.get("rating")
        notes = request.POST.get("notes", "")
        genre = request.POST.get("genre", "")
        mood = request.POST.get("mood", "other")
        recommended_by = request.POST.get("recommended_by", "")
        would_recommend = request.POST.get("would_recommend") == "on"
        watch_later = request.POST.get("watch_later") == "on"

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
                genre=genre,
                mood=mood,
                recommended_by=recommended_by,
                would_recommend=would_recommend,
                watch_later=watch_later,
                watched_at=timezone.now()
            )

        return redirect("/")

    search_query = request.GET.get("search", "").strip()
    service_filter = request.GET.get("service", "").strip()
    reaction_filter = request.GET.get("reaction", "").strip()
    mood_filter = request.GET.get("mood", "").strip()
    watch_later_filter = request.GET.get("watch_later", "").strip()

    watch_items = WatchHistory.objects.all().order_by("-watched_at")

    if search_query:
        watch_items = watch_items.filter(title__icontains=search_query)

    if service_filter:
        watch_items = watch_items.filter(service_name__icontains=service_filter)

    if reaction_filter:
        watch_items = watch_items.filter(reaction=reaction_filter)

    if mood_filter:
        watch_items = watch_items.filter(mood=mood_filter)

    if watch_later_filter == "yes":
        watch_items = watch_items.filter(watch_later=True)

    total_items = WatchHistory.objects.count()
    liked_count = WatchHistory.objects.filter(reaction="liked").count()
    watch_later_count = WatchHistory.objects.filter(watch_later=True).count()
    recommend_count = WatchHistory.objects.filter(would_recommend=True).count()

    average_rating = 0
    rated_items = WatchHistory.objects.exclude(rating__isnull=True)

    if rated_items.exists():
        total_rating = sum(item.rating for item in rated_items if item.rating)
        average_rating = round(total_rating / rated_items.count(), 1)

    displayed_items = watch_items[:75]

    user_options = ""
    for user in users:
        user_options += f'<option value="{user.id}">{user.username}</option>'

    rows = ""
    for item in displayed_items:
        rating_display = item.rating if item.rating else ""
        notes_display = item.notes if item.notes else ""
        recommend_display = "Yes" if item.would_recommend else "No"
        later_display = "Yes" if item.watch_later else "No"

        rows += f"""
        <tr>
            <td>{item.title}</td>
            <td>{item.service_name}</td>
            <td>{item.content_type.title()}</td>
            <td>{item.genre}</td>
            <td>{item.mood.replace("_", " ").title()}</td>
            <td>{item.reaction.title()}</td>
            <td>{rating_display}</td>
            <td>{recommend_display}</td>
            <td>{later_display}</td>
            <td>{item.recommended_by}</td>
            <td>{item.watched_at.strftime('%Y-%m-%d %I:%M %p')}</td>
            <td>{notes_display}</td>
            <td>
                <form method="post" style="margin:0;">
                    <input type="hidden" name="action" value="delete">
                    <input type="hidden" name="item_id" value="{item.id}">
                    <button class="delete" type="submit">Delete</button>
                </form>
            </td>
        </tr>
        """

    if not rows:
        rows = '<tr><td colspan="13" class="empty">No matching watch history found.</td></tr>'

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
                max-width: 1400px;
                margin: 0 auto;
                padding: 32px 20px;
            }}
            .hero {{
                background: linear-gradient(135deg, #1e293b, #111827);
                border-radius: 24px;
                padding: 34px;
                box-shadow: 0 16px 40px rgba(0,0,0,.35);
                margin-bottom: 24px;
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
            p {{
                color: #cbd5e1;
                font-size: 18px;
            }}
            .links {{
                display: flex;
                gap: 12px;
                flex-wrap: wrap;
                margin-top: 20px;
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
                gap: 14px;
                margin-bottom: 24px;
            }}
            .stat {{
                background: #182235;
                border-radius: 18px;
                padding: 18px;
            }}
            .number {{
                font-size: 30px;
                color: #7dd3fc;
                font-weight: bold;
            }}
            .label {{
                color: #cbd5e1;
                font-size: 14px;
            }}
            .card {{
                background: #182235;
                border-radius: 20px;
                padding: 24px;
                margin-bottom: 24px;
                overflow-x: auto;
            }}
            .form-grid, .filter-grid {{
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 14px;
            }}
            .full {{
                grid-column: 1 / -1;
            }}
            label {{
                display: block;
                margin-bottom: 7px;
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
                margin-bottom: 14px;
                box-sizing: border-box;
                font-size: 15px;
            }}
            textarea {{
                min-height: 80px;
            }}
            .checks {{
                display: flex;
                gap: 20px;
                align-items: center;
                margin: 8px 0 18px;
            }}
            .checks label {{
                color: #e5e7eb;
                font-weight: normal;
            }}
            .checks input {{
                width: auto;
                margin-right: 8px;
            }}
            button {{
                background: #7dd3fc;
                color: #082f49;
                border: none;
                padding: 12px 16px;
                border-radius: 12px;
                font-weight: bold;
                cursor: pointer;
            }}
            .delete {{
                background: #fca5a5;
                color: #450a0a;
                padding: 8px 10px;
            }}
            .reset {{
                color: #7dd3fc;
                text-decoration: none;
                font-weight: bold;
                margin-left: 12px;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                min-width: 1300px;
            }}
            th {{
                text-align: left;
                color: #93c5fd;
                border-bottom: 1px solid #334155;
                padding: 10px;
            }}
            td {{
                border-bottom: 1px solid #263244;
                padding: 10px;
                color: #e5e7eb;
                vertical-align: top;
            }}
            .empty {{
                text-align: center;
                color: #94a3b8;
                padding: 24px;
            }}
            .footer {{
                color: #94a3b8;
                font-size: 14px;
            }}
            @media (max-width: 900px) {{
                .stats, .form-grid, .filter-grid {{
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
                <p>Track what you watched, where you watched it, who recommended it, your mood, ratings, and what belongs on your watch-later list.</p>
                <div class="links">
                    <a href="/admin/">Django Admin</a>
                    <a href="/api/users/">Users API</a>
                    <a href="/api/watch-history/">Watch History API</a>
                </div>
            </div>

            <div class="stats">
                <div class="stat"><div class="number">{total_items}</div><div class="label">Total Items</div></div>
                <div class="stat"><div class="number">{liked_count}</div><div class="label">Liked</div></div>
                <div class="stat"><div class="number">{watch_later_count}</div><div class="label">Watch Later</div></div>
                <div class="stat"><div class="number">{recommend_count}</div><div class="label">Would Recommend</div></div>
                <div class="stat"><div class="number">{average_rating}</div><div class="label">Average Rating</div></div>
            </div>

            <div class="card">
                <h2>Add Watch Item</h2>
                <form method="post">
                    <div class="form-grid">
                        <div>
                            <label>Title</label>
                            <input type="text" name="title" placeholder="Example: Severance" required>
                        </div>
                        <div>
                            <label>Streaming Service</label>
                            <input type="text" name="service_name" placeholder="Netflix, Hulu, Max, Apple TV+" required>
                        </div>
                        <div>
                            <label>User</label>
                            <select name="user_id" required>{user_options}</select>
                        </div>
                        <div>
                            <label>Content Type</label>
                            <select name="content_type">
                                <option value="movie">Movie</option>
                                <option value="show">Show</option>
                                <option value="episode">Episode</option>
                                <option value="documentary">Documentary</option>
                                <option value="standup">Standup</option>
                                <option value="sports">Sports</option>
                                <option value="youtube">YouTube</option>
                                <option value="other" selected>Other</option>
                            </select>
                        </div>
                        <div>
                            <label>Genre</label>
                            <input type="text" name="genre" placeholder="Comedy, Sci-Fi, Drama">
                        </div>
                        <div>
                            <label>Mood</label>
                            <select name="mood">
                                <option value="chill">Chill</option>
                                <option value="funny">Funny</option>
                                <option value="intense">Intense</option>
                                <option value="dark">Dark</option>
                                <option value="smart">Smart</option>
                                <option value="background">Background</option>
                                <option value="date_night">Date Night</option>
                                <option value="family">Family</option>
                                <option value="weird">Weird</option>
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
                            <input type="number" name="rating" min="1" max="10" placeholder="9">
                        </div>
                        <div>
                            <label>Recommended By</label>
                            <input type="text" name="recommended_by" placeholder="Friend, TikTok, Reddit">
                        </div>
                        <div class="full">
                            <label>Notes</label>
                            <textarea name="notes" placeholder="Why it mattered, who would like it, what mood it fits."></textarea>
                        </div>
                    </div>

                    <div class="checks">
                        <label><input type="checkbox" name="would_recommend">Would Recommend</label>
                        <label><input type="checkbox" name="watch_later">Watch Later</label>
                    </div>

                    <button type="submit">Add to StreamFolio</button>
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
                            <input type="text" name="service" value="{service_filter}" placeholder="Netflix">
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
                            <label>Mood</label>
                            <select name="mood">
                                <option value="">All</option>
                                <option value="chill">Chill</option>
                                <option value="funny">Funny</option>
                                <option value="intense">Intense</option>
                                <option value="dark">Dark</option>
                                <option value="smart">Smart</option>
                                <option value="background">Background</option>
                                <option value="date_night">Date Night</option>
                                <option value="family">Family</option>
                                <option value="weird">Weird</option>
                                <option value="other">Other</option>
                            </select>
                        </div>
                        <div>
                            <label>Watch Later</label>
                            <select name="watch_later">
                                <option value="">All</option>
                                <option value="yes">Watch Later Only</option>
                            </select>
                        </div>
                        <div>
                            <button type="submit">Filter</button>
                            <a class="reset" href="/">Reset</a>
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
                            <th>Genre</th>
                            <th>Mood</th>
                            <th>Reaction</th>
                            <th>Rating</th>
                            <th>Recommend?</th>
                            <th>Later?</th>
                            <th>Recommended By</th>
                            <th>Watched At</th>
                            <th>Notes</th>
                            <th>Delete</th>
                        </tr>
                    </thead>
                    <tbody>{rows}</tbody>
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
    queryset = WatchHistory.objects.all().order_by("-watched_at")
    serializer_class = WatchHistorySerializer
    permission_classes = [AllowAny]
