from rest_framework import viewsets, permissions, decorators, response, status, filters
from django.db.models import Exists, OuterRef
from datetime import datetime, timedelta
from .models import Court, CourtImage, CourtAvailability
from .serializers import (
    CourtSerializer, CourtCreateUpdateSerializer,
    CourtImageSerializer, CourtAvailabilitySerializer,
    CourtListSerializer
)
from .filters import CourtFilter
from bookings.models import Booking
from users.permissions import IsOwnerRole, IsCourtObjectOwner, IsAuthenticatedOrReadOnly, IsAdmin

class CourtViewSet(viewsets.ModelViewSet):
    queryset = Court.objects.filter(is_active=True).select_related('owner').prefetch_related('images', 'availabilities')
    filterset_class = CourtFilter
    filter_backends = [filters.SearchFilter, filters.OrderingFilter,]
    search_fields = ['name', 'description', 'city', 'location', 'sport_type']
    ordering_fields = ['price_per_hour', 'created_at']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.action in ['list', 'retrieve', 'available_slots']:
            return [IsAuthenticatedOrReadOnly()]
        if self.action == 'create':
            # Only users with owner role can create courts
            return [permissions.IsAuthenticated(), IsOwnerRole()]
        if self.action in ['update', 'partial_update', 'destroy']:
            # Must be the court's owner or admin
            return [permissions.IsAuthenticated(), IsCourtObjectOwner() | IsAdmin()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        # Admins can see inactive too (optional)
        user = self.request.user
        if user.is_authenticated and (user.is_staff or getattr(user, "role", "") == "admin"):
            return Court.objects.all().select_related('owner').prefetch_related('images', 'availabilities')
        return super().get_queryset()

    def get_serializer_class(self):
        if self.action == 'list':
            return CourtListSerializer
        if self.action in ["create", "update", "partial_update"]:
            return CourtCreateUpdateSerializer
        return CourtSerializer

    def perform_create(self, serializer):
        # ensure authenticated owner is set as court owner
        serializer.save(owner=self.request.user)

    @decorators.action(detail=True, methods=['get'], url_path='available-slots', permission_classes=[IsAuthenticatedOrReadOnly])
    def available_slots(self, request, pk=None):
        court = self.get_object()
        date_str = request.query_params.get('date')
        if not date_str:
            return response.Response({"detail": "date is required (YYYY-MM-DD)."},
                                     status=status.HTTP_400_BAD_REQUEST)

        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        weekday_name = booking_date.strftime("%A").lower()

        day_avails = court.availabilities.filter(day_of_week=weekday_name).order_by('start_time')
        if not day_avails.exists():
            return response.Response({"date": date_str, "slots": []})

        bookings = Booking.objects.filter(
            court=court,
            booking_date=booking_date,
            status__in=['pending', 'confirmed']
        ).order_by('start_time')

        def to_dt(t): return datetime.combine(booking_date, t)
        increments = timedelta(minutes=30)
        free_slots = []

        for av in day_avails:
            window_start = to_dt(av.start_time)
            window_end = to_dt(av.end_time)

            busy = []
            for b in bookings:
                b_start = to_dt(b.start_time)
                b_end = to_dt(b.end_time)
                if b_end <= window_start or b_start >= window_end:
                    continue
                busy.append((max(window_start, b_start), min(window_end, b_end)))
            busy.sort()
            merged = []
            for s, e in busy:
                if not merged or s > merged[-1][1]:
                    merged.append((s, e))
                else:
                    merged[-1] = (merged[-1][0], max(merged[-1][1], e))

            cursor = window_start
            for s, e in merged:
                if cursor < s:
                    free_slots.append((cursor, s))
                cursor = max(cursor, e)
            if cursor < window_end:
                free_slots.append((cursor, window_end))

        discrete = []
        for s, e in free_slots:
            cur = s
            while cur + increments <= e:
                discrete.append({
                    "start": cur.strftime("%H:%M"),
                    "end": (cur + increments).strftime("%H:%M")
                })
                cur += increments

        return response.Response({"date": date_str, "slot_size_minutes": 30, "slots": discrete})


class CourtImageViewSet(viewsets.ModelViewSet):
    queryset = CourtImage.objects.select_related('court')
    serializer_class = CourtImageSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsOwnerRole()]
        # For update/delete: must own the underlying court or be admin
        return [permissions.IsAuthenticated(), IsCourtObjectOwner() | IsAdmin()]

    def perform_create(self, serializer):
        court_id = self.request.data.get("court")
        # Enforce: you can only upload to your own court
        from .models import Court
        court = Court.objects.get(pk=court_id)
        if court.owner_id != self.request.user.id and not (self.request.user.is_staff or getattr(self.request.user, "role", "") == "admin"):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only upload images for your own court.")
        serializer.save(court=court)


class CourtAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = CourtAvailability.objects.select_related('court')
    serializer_class = CourtAvailabilitySerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticatedOrReadOnly()]
        if self.action == 'create':
            return [permissions.IsAuthenticated(), IsOwnerRole()]
        # For update/delete: must own the court or be admin
        return [permissions.IsAuthenticated(), IsCourtObjectOwner() | IsAdmin()]

    def perform_create(self, serializer):
        court_id = self.request.data.get("court")
        from .models import Court
        court = Court.objects.get(pk=court_id)
        if court.owner_id != self.request.user.id and not (self.request.user.is_staff or getattr(self.request.user, "role", "") == "admin"):
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You can only set availability for your own court.")
        serializer.save(court=court)
