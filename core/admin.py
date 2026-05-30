from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, WatchHistory


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')


@admin.register(WatchHistory)
class WatchHistoryAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'service_name',
        'content_type',
        'genre',
        'mood',
        'reaction',
        'rating',
        'would_recommend',
        'watch_later',
        'watched_at',
        'user',
    )
    list_filter = (
        'service_name',
        'content_type',
        'genre',
        'mood',
        'reaction',
        'rating',
        'would_recommend',
        'watch_later',
        'watched_at',
    )
    search_fields = (
        'title',
        'service_name',
        'genre',
        'notes',
        'recommended_by',
        'user__username',
    )
