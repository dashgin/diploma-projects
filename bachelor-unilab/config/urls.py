import requests
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views import defaults as default_views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework import status
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Auth
class AccessTokenView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0]) from e
        serializer.validated_data.pop("refresh", None)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def get_user(request):
    token = request.POST.get("token")
    if not token:
        return Response({"response": None, "error": "no token given"})
    try:
        validated_token = JWTAuthentication().get_validated_token(token)
        user_object = JWTAuthentication().get_user(validated_token)
        response = requests.get(
            f"{settings.API_URL}/api/users/{user_object.id}",
            headers={"Authorization": f"Bearer {token}"},
        )
        return Response({"response": response.json()})
    except InvalidToken as ex:
        return Response({"response": None, "error": ex.detail["detail"]})
    except Exception as ex:
        return Response({"response": None, "error": "unknown error"})


urlpatterns += [
    path("api/token", AccessTokenView.as_view(), name="token_obtain"),
    path("api/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/token/validate", TokenVerifyView.as_view(), name="token_verify"),
    path("api/token/get-user", get_user, name="get-user"),
]
# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    # DRF auth token
    path("auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="api-schema"),
        name="api-redoc",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
