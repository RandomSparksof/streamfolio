from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, WatchHistoryViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'watch-history', WatchHistoryViewSet, basename='watchhistory')

urlpatterns = [
    path('api/', include(router.urls)),
]
