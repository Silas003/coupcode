from rest_framework import serializers, exceptions
from .models import CustomUser as User, Profile
from django.contrib import auth
from django.db import transaction



class UserCreationSerializer(serializers.ModelSerializer):

    def validate(self, data):
        username = data.get("username")
        user = User.objects.filter(username=username).first()

        if user is not None:
            raise exceptions.ValidationError("Username already in use")
        return data

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
        )


class UserViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", )
        read_only = True


class VerifyAccountSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.IntegerField()

    def validate_email(self, email):
        if email:
            user = User.objects.get(email=email)
            if not user:
                raise exceptions.ValidationError("User with this email does not exist")
            return user
        return None

    def validate(self, attrs):
        email = self.initial_data.get("email")
        otp = self.initial_data.get("otp")
        user = User.objects.filter(email=email).first()
        if not user:
            raise exceptions.ValidationError("User does not exist")

        if not user.otp_expiry:
            raise exceptions.ValidationError("user  otp has expired")
        if len(user.otp) < 5 or int(user.otp) != int(otp):
            raise exceptions.ValidationError("Invalid otp")

        return attrs

    @transaction.atomic
    def save(
        self,
    ):
        email = self.initial_data.get("email")
        otp = self.initial_data.get("otp")

        user = User.objects.get(email=email)
        if user is not None:
            if user.otp == otp:
                user.is_active = True
                user.save()
        return user


class ResendOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                raise exceptions.ValidationError("User does not exist")
            return user
        return None

    def validate(self, attrs):
        email = self.initial_data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            raise exceptions.ValidationError("User does not exist")
        return attrs

    @transaction.atomic
    def save(self):
        email = self.initial_data.get("email")
        user = User.objects.get(email=email)
        if user is not None:
            return user

        return None


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    otp = serializers.IntegerField()

    def validate_email(self, email):
        self.email = email
        if email:
            user = User.objects.filter(email=self.email).first()
            if not user:
                raise exceptions.ValidationError("User does not exist1")
            return user
        return None

    def validate_password(self, password):
        if password:
            if len(password) < 8:
                raise exceptions.ValidationError(
                    "Password must be at least 8 characters"
                )

        return None

    def validate(self, attrs):
        email = self.initial_data.get("email")
        otp = self.initial_data.get("otp")
        user = User.objects.filter(email=email).first()
        if not user:
            raise exceptions.ValidationError("User does not exist")
        if not user.otp_expiry:
            raise exceptions.ValidationError("user  otp has expired")
        if int(user.otp) < 6 or int(user.otp) != int(otp):
            raise exceptions.ValidationError("Invalid otp")
        return attrs

    @transaction.atomic
    def save(self):
        email = self.initial_data.get("email")
        password = self.initial_data.get("password")
        user = User.objects.filter(email=email).first()
        user.set_password(password)
        user.save()
        return user


class ResetPasswordOtpSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if email:
            user = User.objects.filter(email=email).first()
            if not user:
                raise exceptions.ValidationError("User does not exist")
            return user
        return None

    def validate(self, attrs):
        email = self.initial_data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            raise exceptions.ValidationError("User does not exist")

        return attrs

    @transaction.atomic
    def save(self):
        email = self.initial_data.get("email")
        user = User.objects.get(email=email)
        if user is not None:
            return user
        return None


class ProfileSerializer(serializers.ModelSerializer):

    def validate(self, data):
        username = data.get("display_name")
        user = Profile.objects.filter(display_name=username).first()

        if user is not None:
            raise exceptions.ValidationError("Username already in use")
        return data

    class Meta:
        model = Profile
        fields = "__all__"


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=68, min_length=4, write_only=True)
    username = serializers.CharField(max_length=255, min_length=3, read_only=True)

    tokens = serializers.SerializerMethodField()

    def get_tokens(self, obj):
        user = User.objects.get(email=obj["email"])

        return {"refresh": user.tokens()["refresh"], "access": user.tokens()["access"]}

    class Meta:
        model = User
        fields = ["email", "password", "username", "tokens"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")
        user = auth.authenticate(email=email, password=password)
        if not user:
            raise exceptions.AuthenticationFailed("Invalid credentials, try again")
        if not user.is_active:
            raise exceptions.AuthenticationFailed("Account disabled, contact admin")
        # if not user.is_verified:
        #     raise exceptions.AuthenticationFailed("Email is not verified")

        return {"email": user.email, "username": user.username, "tokens": user.tokens}

