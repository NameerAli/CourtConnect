from django.contrib.auth.models import AbstractUser
from django.db import models
from common.models import BaseModel  # If you created BaseModel


class User(AbstractUser, BaseModel):
    ROLE_CHOICES = (
        ("player", "Player"),
        ("owner", "Court Owner"),
        ("admin", "Admin"),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="player")

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='user_set_custom',
        related_query_name='user_custom',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='user_set_custom',
        related_query_name='user_custom',
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
