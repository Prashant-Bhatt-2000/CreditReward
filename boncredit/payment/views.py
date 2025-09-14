from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from decimal import Decimal, ROUND_DOWN, InvalidOperation
from uuid import uuid4
from .models import CreditModel, PaymentModel
from .serializer import PaymentSerializer


import uuid

class CreatePaymentOrderAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        user = request.user
        credit_id = request.data.get("credit_id")
        amount_raw = request.data.get("amount")

        # Validate required fields
        if not credit_id or amount_raw is None:
            return Response(
                {"error": "Credit ID and amount are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = Decimal(str(amount_raw))
            amount = amount.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
        except (InvalidOperation, ValueError):
            return Response(
                {"error": "Invalid amount format"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check max_digits=10, decimal_places=2
        if amount <= 0:
            return Response(
                {"error": "Amount must be greater than zero"},
                status=status.HTTP_400_BAD_REQUEST
            )

        digits_before_decimal = len(str(amount.to_integral()))
        if digits_before_decimal > 8:  # max_digits - decimal_places = 10 - 2 = 8
            return Response(
                {"error": "Amount exceeds max allowed digits (10 total with 2 decimals)"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Fetch the credit
        try:
            credit = CreditModel.objects.get(id=credit_id, user=user)
        except CreditModel.DoesNotExist:
            return Response(
                {"error": "Credit not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        # Create payment
        payment = PaymentModel.objects.create(
            user=user,
            credit=credit,
            amount=amount,
            status="PENDING",
            # order_id=str(uuid4())
        )

        serializer = PaymentSerializer(payment)

        return Response({
            "message": "Payment order created successfully",
            "payment": serializer.data
        }, status=status.HTTP_201_CREATED)



class VerifyPaymentAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        
        data = request.data
        payment_id = data.get("payment_id")
        credit_id = data.get("credit_id")

        if not payment_id or not credit_id:
            return Response({"error": "Payment ID and Credit ID are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            payment = PaymentModel.objects.get(
                id=payment_id, credit__id=credit_id, user=request.user, status="PENDING"
            )
        except PaymentModel.DoesNotExist:
            return Response({"error": "Payment record not found or already verified"},
                            status=status.HTTP_404_NOT_FOUND)

        payment.status = "COMPLETED"
        payment.save()

        return Response({"message": "Payment verified successfully"},
                        status=status.HTTP_200_OK)
