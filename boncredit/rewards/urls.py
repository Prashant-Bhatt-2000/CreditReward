from django.urls import path
from .views import RewardListAPIView, AllRewardListAPIView, ClaimRewardAPIView

urlpatterns = [
    path('rewards', RewardListAPIView.as_view(), name='reward-list-create'),
    path('allrewards', AllRewardListAPIView.as_view(), name='all_rewards-list'),
    path('claimreward', ClaimRewardAPIView.as_view(), name='claim-reward')
]
