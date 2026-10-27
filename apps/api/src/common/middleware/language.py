"""Custom middleware for the common app."""

import typing as t

from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.utils import translation


class UserLanguageMiddleware:
    """Keep the administration in Spanish and honor account language elsewhere.

    NOTE: This middleware is NOT used for JWT authentication. For JWT-authenticated requests,
    language activation happens in the I18nJWTAuth authentication class (see common.authentication).

    This middleware is only useful if you add session-based authentication in the future.
    For JWT-only APIs (like this project), language is activated during JWT authentication,
    not in middleware.

    This middleware should be placed after AuthenticationMiddleware and LocaleMiddleware.
    It overrides the language detected by LocaleMiddleware with the user's saved preference.
    """

    def __init__(self, get_response: t.Callable[[HttpRequest], HttpResponse]) -> None:
        """Initialize the middleware.

        Args:
            get_response: The next middleware or view in the chain
        """
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        """Process the request and activate user's preferred language.

        Args:
            request: The HTTP request

        Returns:
            The HTTP response
        """
        admin_prefix = "/" + settings.ADMIN_URL.strip("/") + "/"
        if settings.ADMIN_URL and (
            request.path_info == admin_prefix.rstrip("/") or request.path_info.startswith(admin_prefix)
        ):
            translation.activate("es")
            request.LANGUAGE_CODE = "es"
        elif hasattr(request, "user") and request.user.is_authenticated:
            user_language = getattr(request.user, "language", None)
            if user_language:
                translation.activate(user_language)
                request.LANGUAGE_CODE = user_language

        response = self.get_response(request)

        # Deactivate to avoid side effects
        translation.deactivate()

        return response
