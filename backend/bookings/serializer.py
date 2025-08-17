from rest_framework import serializers
from .models import Booking
from courts.models import Court
from datetime import datetime


class BookingSerializer(serializers.ModelSerializer):
    court_name = serializers.CharField(source="court.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Booking
        fields = [
            "id",
            "court",
            "court_name",
            "user",
            "user_email",
            "booking_date",
            "start_time",
            "end_time",
            "status",
            "total_price",
        ]
        read_only_fields = ["status", "total_price"]

    def validate(self, data):
        """Ensure booking is within court availability & no overlap"""
        court = data["court"]
        booking_date = data["booking_date"]
        start_time = data["start_time"]
        end_time = data["end_time"]

        if start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time.")

        # check overlaps with existing bookings
        existing_bookings = Booking.objects.filter(
            court=court, booking_date=booking_date, status__in=["pending", "confirmed"]
        )

        for booking in existing_bookings:
            if not (end_time <= booking.start_time or start_time >= booking.end_time):
                raise serializers.ValidationError("This slot is already booked.")

        # price calculation
        duration_hours = (
            datetime.combine(booking_date, end_time)
            - datetime.combine(booking_date, start_time)
        ).seconds / 3600
        data["total_price"] = duration_hours * float(court.price_per_hour)

        # No past-dated bookings
        if booking_date < date.today():
            raise serializers.ValidationError("Booking date cannot be in the past.")

        # Same-day: no past time
        if booking_date == date.today():
            if datetime.combine(booking_date, end_time) <= now():
                raise serializers.ValidationError("Time window must be in the future.")

        return data

    def create(self, validated_data):
        booking = Booking.objects.create(**validated_data)
        return booking
