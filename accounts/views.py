from rest_framework import viewsets, status, permissions
from .models import CustomUser as User, Profile
from .serializers import *
from helper import utils
from .tasks import send_mail
from rest_framework.response import Response
from datetime import  timedelta
from rest_framework.generics import GenericAPIView
import os
from django.utils import timezone


class UserCreationView(viewsets.ModelViewSet):
    serializer_class = UserCreationSerializer
    queryset = User.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        else:
            return [permissions.IsAuthenticated()]
        
    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return UserViewSerializer
        else:
            return UserCreationSerializer

    def create(self, request, *args, **kwargs):
        serializer = UserCreationSerializer(data=request.data)
        # check  if the serializer is valid before saving


        serializer.is_valid(raise_exception=True)
        user: User = serializer.save()

        # hash the password
        user.set_password(request.data.get("password"))
        user.otp = utils.generate_otp()
        user.otp_expiry = timezone.now() + timedelta(minutes=7)
        user.save()
        profile=Profile.objects.create(user=user,display_name=user.username)
        profile.save()
        # send verification email to user's email address
        # send_mail.delay(user.id)
        serialized_user = UserViewSerializer(instance=user)
        return Response(data=serialized_user.data, status=status.HTTP_201_CREATED)


class ProfileView(viewsets.ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class VerifyAccountView(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class = VerifyAccountSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = VerifyAccountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "email": serializer.data.get("email"),
                "status": "Account verified successfully",
            },
            status=status.HTTP_200_OK,
        )


class ResendOtpView(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class = ResendOtpSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ResendOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = User.objects.filter(email=request.data.get("email")).first()
        user.otp = utils.generate_otp()
        user.otp_expiry = timezone.now() + timedelta(minutes=7)
        user.save()

        send_mail.delay(user.id)
        return Response(
            {"email": request.data.get("email"), "status": "OTP resend successful"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordOtpView(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class = ResetPasswordOtpSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ResetPasswordOtpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = User.objects.filter(email=request.data.get("email")).first()
        user.otp = utils.generate_otp()
        user.otp_expiry = timezone.now() + timedelta(minutes=7)
        user.save()

        send_mail.delay(user.id)
        return Response(
            {"email": request.data.get("email"), "status": "OTP resend successful"},
        )


class ResetPasswordView(viewsets.ModelViewSet):
    permission_classes=[permissions.AllowAny]
    serializer_class = ResetPasswordSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user = User.objects.filter(email=request.data.get("email")).first()

        send_mail.delay(user.id)
        return Response(
            {"email": request.data.get("email"), "status": "Password Reset complete"},
            status=status.HTTP_200_OK,
        )


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes=[permissions.AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


