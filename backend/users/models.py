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

    def __str__(self):
        return f"{self.username} ({self.role})"
