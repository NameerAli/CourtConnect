from rest_framework import serializers
from .models import Court, CourtImage, CourtAvailability


class CourtImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtImage
        fields = ["id", "image"]


class CourtAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = CourtAvailability
        fields = ["id", "day_of_week", "start_time", "end_time"]


class CourtSerializer(serializers.ModelSerializer):
    images = CourtImageSerializer(many=True, read_only=True)
    availabilities = CourtAvailabilitySerializer(many=True, read_only=True)

    class Meta:
        model = Court
        fields = [
            "id",
            "name",
            "sport_type",
            "description",
            "location",
            "price_per_hour",
            "capacity",
            "is_active",
            "images",
            "availabilities",
        ]


class CourtCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = [
            "name",
            "sport_type",
            "description",
            "location",
            "price_per_hour",
            "capacity",
            "is_active",
        ]


class CourtListSerializer(serializers.ModelSerializer):
    first_image = serializers.SerializerMethodField()

    class Meta:
        model = Court
        fields = [
            "id",
            "name",
            "sport_type",
            "city",
            "location",
            "price_per_hour",
            "capacity",
            "is_active",
            "first_image",
        ]

    def get_first_image(self, obj):
        img = obj.images.first()
        return img.image.url if img else None


# Keep your existing CourtSerializer, CourtImageSerializer, CourtAvailabilitySerializer, etc.
