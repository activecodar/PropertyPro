from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.authentication.api.views import (RegistrationViewSet, LoginView,
                                           PasswordResetRequestView, PasswordResetView)

router = DefaultRouter(trailing_slash=False)
router.register(r'users', RegistrationViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path("login", LoginView.as_view(), name="login"),
    path("password-reset-request", PasswordResetRequestView.as_view(), name="password-reset-request"),
    path("password-reset/<str:token>", PasswordResetView.as_view(), name="password-reset")
]
