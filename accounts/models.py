from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from uuid import uuid4

class CustomUser(AbstractUser):
    id=models.UUIDField(primary_key=True,default=uuid4)
    email=models.EmailField(unique=True)
    otp = models.CharField(max_length=7)
    otp_expiry = models.DateTimeField(auto_now_add=True)


    REQUIRED_FIELDS = ["username"]
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

class Profile(models.Model):

    user = models.OneToOneField(
        CustomUser, related_name="users", on_delete=models.CASCADE
    )
    display_name = models.CharField(max_length=100, blank=True, null=True)
    amount_won=models.FloatField(null=True, blank=True, default=0.0)

    def __str__(self):
        return f"{self.display_name}"
