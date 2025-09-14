from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4

from .models import User
from .emailverify import sendemail  


# -----------------------------
# SIGN UP                      |
# -----------------------------
class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, email):
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email already exists")
        return email

    def create(self, validated_data):
        # Hash password
        validated_data['password'] = make_password(validated_data['password'])
        
        # Create verification token
        token = str(uuid4())
        validated_data['verification_token'] = token

        # Send verification email
        # sendemail(validated_data['email'], token)

        return User.objects.create(**validated_data)


# -----------------------------
# SIGN IN                      |
# -----------------------------
class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            raise serializers.ValidationError('Email and password are required.')

        # Authenticate user
        user = authenticate(
            request=self.context.get('request'), 
            email=email, 
            password=password
        )
        if not user:
            raise serializers.ValidationError('Incorrect email or password.')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled.')

        refresh = RefreshToken.for_user(user)
        return {
            'message': 'Login successful.',
            'username': user.name,
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


# -----------------------------
# PASSWORD RESET REQUEST       |
# -----------------------------
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("No account associated with this email")
        return email

    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = str(uuid4())
        user.password_reset_token = token
        user.save()
        # send email with reset link
        sendemail(email, token)


# -----------------------------
# RESET PASSWORD               |
# -----------------------------
class PasswordResetSerializer(serializers.Serializer):
    token = serializers.CharField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match")

        if not User.objects.filter(password_reset_token=data['token']).exists():
            raise serializers.ValidationError("Invalid or expired token")

        return data

    def save(self):
        token = self.validated_data['token']
        user = User.objects.get(password_reset_token=token)
        user.password = make_password(self.validated_data['password'])
        user.password_reset_token = None  # invalidate token
        user.save()
        return user
