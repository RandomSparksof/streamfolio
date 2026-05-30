from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)


class WatchHistory(models.Model):
    CONTENT_TYPE_CHOICES = [
        ('movie', 'Movie'),
        ('show', 'Show'),
        ('episode', 'Episode'),
        ('documentary', 'Documentary'),
        ('standup', 'Standup'),
        ('sports', 'Sports'),
        ('youtube', 'YouTube'),
        ('other', 'Other'),
    ]

    REACTION_CHOICES = [
        ('liked', 'Liked'),
        ('neutral', 'Neutral'),
        ('disliked', 'Disliked'),
    ]

    MOOD_CHOICES = [
        ('chill', 'Chill'),
        ('funny', 'Funny'),
        ('intense', 'Intense'),
        ('dark', 'Dark'),
        ('smart', 'Smart'),
        ('background', 'Background'),
        ('date_night', 'Date Night'),
        ('family', 'Family'),
        ('weird', 'Weird'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    service_name = models.CharField(max_length=100)
    watched_at = models.DateTimeField()
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES, default='other')
    reaction = models.CharField(max_length=50, choices=REACTION_CHOICES, default='neutral')
    rating = models.PositiveSmallIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    genre = models.CharField(max_length=100, blank=True)
    mood = models.CharField(max_length=50, choices=MOOD_CHOICES, default='other')
    recommended_by = models.CharField(max_length=100, blank=True)
    would_recommend = models.BooleanField(default=False)
    watch_later = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.title} - {self.service_name}'
