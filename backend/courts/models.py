from django.db import models
from django.conf import settings
from common.models import BaseModel # Assuming BaseModel is defined in common.models

User = settings.AUTH_USER_MODEL

class Court(BaseModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="courts")
    name = models.CharField(max_length=255)
    sport_type = models.CharField(
        max_length=100,
        choices=[
            ("paddle", "Paddle"),
            ("badminton", "Badminton"),
            ("table_tennis", "Table Tennis"),
            ("indoor_cricket", "Indoor Cricket"),
            ("basketball", "Basketball"),
            ("other", "Other"),
        ]
    )
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    price_per_hour = models.DecimalField(max_digits=8, decimal_places=2)
    capacity = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    # add these fields to Court if useful for filtering/map
    city = models.CharField(max_length=80, blank=True, default="")
    lat = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    lng = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['sport_type']),
            models.Index(fields=['city']),
            models.Index(fields=['price_per_hour']),
        ]

    def __str__(self):
        return f"{self.name} - {self.sport_type}"


class CourtImage(BaseModel):
    court = models.ForeignKey(Court, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="court_images/")

    def __str__(self):
        return f"Image for {self.court.name}"


class CourtAvailability(BaseModel):
    court = models.ForeignKey(Court, related_name="availabilities", on_delete=models.CASCADE)
    day_of_week = models.CharField(
        max_length=10,
        choices=[
            ("monday", "Monday"),
            ("tuesday", "Tuesday"),
            ("wednesday", "Wednesday"),
            ("thursday", "Thursday"),
            ("friday", "Friday"),
            ("saturday", "Saturday"),
            ("sunday", "Sunday"),
        ]
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.court.name} - {self.day_of_week} ({self.start_time}-{self.end_time})"
