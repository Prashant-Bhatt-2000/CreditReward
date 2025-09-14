from django.urls import path
from .views import (
    SignUpAPIView,
    SignInAPIView,
    VerifyEmailAPIView,
    PasswordResetRequestAPIView,
    PasswordResetAPIView,
)

urlpatterns = [
    path("signup/", SignUpAPIView.as_view(), name="signup"),
    path("signin/", SignInAPIView.as_view(), name="signin"),
    path("verify/<uuid:token>/", VerifyEmailAPIView.as_view(), name="verify-email"),
    path("password-reset-request/", PasswordResetRequestAPIView.as_view(), name="password-reset-request"),
    path("reset-password/", PasswordResetAPIView.as_view(), name="reset-password"),
]
