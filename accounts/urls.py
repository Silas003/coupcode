from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

app_name = "accounts"


router = DefaultRouter()

router.register("register", viewset=views.UserCreationView, basename="register")
router.register("verify", viewset=views.VerifyAccountView, basename="verify")
router.register("profile", viewset=views.ProfileView, basename="profile")
router.register("resendotp", viewset=views.ResendOtpView, basename="resendotp")
router.register("resetotp", viewset=views.ResetPasswordOtpView, basename="resetotp")
router.register("reset", viewset=views.ResetPasswordView, basename="reset")

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns += router.urls
