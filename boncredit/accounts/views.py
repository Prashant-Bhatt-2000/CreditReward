from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.decorators import method_decorator

from .models import User
from .serializer import (
    SignUpSerializer,
    SignInSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)


# -----------------------------
# SIGN UP VIEW
# -----------------------------
class SignUpAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"message": "Account created successfully. Please verify your email."},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# VERIFY EMAIL VIEW
# -----------------------------
class VerifyEmailAPIView(APIView):

    def get(self, request, token, *args, **kwargs):
        user = get_object_or_404(User, verification_token=token)
        if user.is_verified:
            return Response({"message": "Account already verified."}, status=status.HTTP_200_OK)

        user.is_verified = True
        user.verification_token = None
        user.save()
        return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)


# -----------------------------
# SIGN IN VIEW
# -----------------------------
class SignInAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = SignInSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# PASSWORD RESET REQUEST VIEW
# -----------------------------
class PasswordResetRequestAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset link sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# -----------------------------
# RESET PASSWORD VIEW
# -----------------------------
class PasswordResetAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password has been reset successfully."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
