# users/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or getattr(request.user, "role", "") == "admin")
        )


class IsOwnerRole(BasePermission):
    """User has the 'owner' role (not object owner check)."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", "") == "owner"
        )


class IsPlayerRole(BasePermission):
    """User has the 'player' role."""

    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "role", "") == "player"
        )


class IsCourtObjectOwner(BasePermission):
    """Object-level check: the object's owner is the request.user.
    Works for Court objects directly, and for related objects that have .court (e.g., CourtImage, CourtAvailability).
    """

    def has_object_permission(self, request, view, obj):
        # direct Court
        if hasattr(obj, "owner"):
            return obj.owner_id == request.user.id
        # nested models with .court
        if hasattr(obj, "court") and hasattr(obj.court, "owner_id"):
            return obj.court.owner_id == request.user.id
        return False
