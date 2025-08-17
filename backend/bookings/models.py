from django.db import models
from django.conf import settings
from common.models import BaseModel
from courts.models import Court

User = settings.AUTH_USER_MODEL


class Booking(BaseModel):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    court = models.ForeignKey(Court, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    class Meta:
        indexes = [
            models.Index(fields=["court", "booking_date"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.court.name} ({self.booking_date} {self.start_time}-{self.end_time})"
