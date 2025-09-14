from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from .models import CreditModel
from .serializer import CreditRequestSerializer, CreditViewSerializer

class RequestCreditView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = CreditRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            credit = serializer.save()
            return Response({
                'message': 'Credit request submitted successfully.',
                'credit_id': credit.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MyCreditsView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        credits = CreditModel.objects.filter(user=request.user).order_by('-created_at')
        serializer = CreditViewSerializer(credits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
