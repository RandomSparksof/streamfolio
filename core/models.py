from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='watch_history')
    title = models.CharField(max_length=255)
    watched_at = models.DateTimeField()
    service_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['-watched_at']

    def __str__(self):
        return f"{self.user.username} — {self.title} ({self.service_name})"
