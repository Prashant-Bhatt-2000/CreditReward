from django.urls import path, include

urlpatterns = [
    path("accounts/", include("accounts.urls")),
    path("credit/", include("credit.urls")),
    path("payment/", include("payment.urls")),
    path("rewards/", include("rewards.urls"))
] 