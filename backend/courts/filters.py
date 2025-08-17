# courts/filters.py
import django_filters as df
from django.db.models import Exists, OuterRef, Q
from datetime import datetime
from .models import Court, CourtAvailability
from bookings.models import Booking


class CourtFilter(df.FilterSet):
    # primitives
    sport_type = df.CharFilter(field_name="sport_type", lookup_expr="iexact")
    city = df.CharFilter(field_name="city", lookup_expr="icontains")
    price_min = df.NumberFilter(field_name="price_per_hour", lookup_expr="gte")
    price_max = df.NumberFilter(field_name="price_per_hour", lookup_expr="lte")

    # availability params (expect query params: date=YYYY-MM-DD&start=HH:MM&end=HH:MM)
    date = df.DateFilter(method="filter_available")
    start = df.TimeFilter(method="filter_available")
    end = df.TimeFilter(method="filter_available")

    class Meta:
        model = Court
        fields = ["sport_type", "city", "price_min", "price_max"]

    def filter_available(self, queryset, name, value):
        """
        When any of date/start/end are present, enforce:
        1) Court has an availability window that fully covers [start, end] on that weekday.
        2) There is NO booking that overlaps [start, end] for that court on that date (pending/confirmed).
        """
        request = self.request
        date_str = request.query_params.get("date")
        start_str = request.query_params.get("start")
        end_str = request.query_params.get("end")

        if not (date_str and start_str and end_str):
            return queryset

        # parse
        booking_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_time = datetime.strptime(start_str, "%H:%M").time()
        end_time = datetime.strptime(end_str, "%H:%M").time()

        if start_time >= end_time:
            # invalid window -> return empty
            return queryset.none()

        weekday_name = booking_date.strftime("%A").lower()  # e.g., 'monday'

        # 1) availability window covers the requested range
        avail_qs = CourtAvailability.objects.filter(
            court=OuterRef("pk"),
            day_of_week=weekday_name,
            start_time__lte=start_time,
            end_time__gte=end_time,
        )

        # 2) no overlapping bookings on that date
        overlap = Booking.objects.filter(
            court=OuterRef("pk"),
            booking_date=booking_date,
            status__in=["pending", "confirmed"],
        ).filter(~(Q(end_time__lte=start_time) | Q(start_time__gte=end_time)))

        return queryset.annotate(
            has_covering_avail=Exists(avail_qs),
            has_overlap=Exists(overlap),
        ).filter(
            has_covering_avail=True,
            has_overlap=False,
            is_active=True,
        )
