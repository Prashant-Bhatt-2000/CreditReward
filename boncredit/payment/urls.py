from django.urls import path
from .views import CreatePaymentOrderAPIView, VerifyPaymentAPIView

urlpatterns = [
    path("paycredit/", CreatePaymentOrderAPIView.as_view(), name="create-payment-order"),
    path("verify-payment/", VerifyPaymentAPIView.as_view(), name="verify-payment"),
]
