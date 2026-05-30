from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404, render
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

    context = {
        "users": users,
        "watch_items": watch_items[:75],
        "total_items": total_items,
        "liked_count": liked_count,
        "watch_later_count": watch_later_count,
        "recommend_count": recommend_count,
        "average_rating": average_rating,
        "search_query": search_query,
        "service_filter": service_filter,
        "reaction_filter": reaction_filter,
        "mood_filter": mood_filter,
        "watch_later_filter": watch_later_filter,
    }

    return render(request, "core/home.html", context)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class WatchHistoryViewSet(viewsets.ModelViewSet):
    queryset = WatchHistory.objects.all().order_by("-watched_at")
    serializer_class = WatchHistorySerializer
    permission_classes = [AllowAny]
