from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Booking
from .serializers import BookingSerializer
from users.permissions import IsPlayerRole, IsAdmin
from courts.models import Court

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.select_related('court', 'user')

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        if self.action == 'create':
            # Only players can create bookings
            return [permissions.IsAuthenticated(), IsPlayerRole()]
        # updates/cancels: player can modify their own; owner/admin can manage
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if not user.is_authenticated:
            return Booking.objects.none()

        # Admin sees all
        if user.is_staff or getattr(user, "role", "") == "admin":
            return Booking.objects.all().select_related('court', 'user')

        # Owners see bookings for their courts
        if getattr(user, "role", "") == "owner":
            return Booking.objects.filter(court__owner=user).select_related('court', 'user')

        # Players see only their bookings
        return Booking.objects.filter(user=user).select_related('court', 'user')

    def perform_create(self, serializer):
        court: Court = serializer.validated_data["court"]
        # Optional: block owners from booking their own courts
        if getattr(self.request.user, "role", "") != "player":
            raise PermissionDenied("Only players can create bookings.")
        serializer.save(user=self.request.user)
