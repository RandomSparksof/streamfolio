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
        ('other', 'Other'),
    ]

    REACTION_CHOICES = [
        ('liked', 'Liked'),
        ('neutral', 'Neutral'),
        ('disliked', 'Disliked'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    service_name = models.CharField(max_length=100)
    watched_at = models.DateTimeField()
    content_type = models.CharField(
        max_length=50,
        choices=CONTENT_TYPE_CHOICES,
        default='other'
    )
    reaction = models.CharField(
        max_length=50,
        choices=REACTION_CHOICES,
        default='neutral'
    )
    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text='Optional rating from 1 to 10'
    )
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.title} - {self.service_name}'
