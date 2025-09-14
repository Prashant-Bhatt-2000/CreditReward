from django.urls import path
from .views import RequestCreditView, MyCreditsView

urlpatterns = [
    path("request_credit/", RequestCreditView.as_view(), name="credit_request"),
    path("mycredits/", MyCreditsView.as_view(), name="credit_request"),
]
