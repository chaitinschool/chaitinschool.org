from django.contrib.auth import mixins
from django.core.exceptions import PermissionDenied


class SuperuserRequiredMixin(mixins.AccessMixin):
    """Verify that the current user is authenticated and a superuser."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise PermissionDenied()
        return super().dispatch(request, *args, **kwargs)
