from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import RewardModel
from .serializer import RewardSerializer
from credit.models import CreditModel
from payment.models import PaymentModel
from django.utils import timezone

class RewardListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rewards = RewardModel.objects.filter(user=request.user, is_claimed=False)
        serializer = RewardSerializer(rewards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AllRewardListAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        rewards = RewardModel.objects.filter(user=request.user)
        serializer = RewardSerializer(rewards, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ClaimRewardAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, reward_id, *args, **kwargs):
        try:
            reward = RewardModel.objects.get(id=reward_id, user=request.user, is_claimed=False)
        except RewardModel.DoesNotExist:
            return Response({"error": "Reward not found or already claimed"}, status=status.HTTP_404_NOT_FOUND)

        reward.is_claimed = True
        reward.save()

        # we can delete but I am preferring it to show it as claimed
        # reward.delete()

        return Response({
            "message": "Reward claimed successfully!",
            "reward": RewardSerializer(reward).data
        }, status=status.HTTP_200_OK)
