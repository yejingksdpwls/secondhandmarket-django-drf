from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.AccountAPIView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
    path("logout/", views.LogoutAPIView.as_view(), name="logout"),
    path("password/", views.PasswordChangeAPIView.as_view(), name="password"),
    path("<str:username>/", views.ProfileAPIView.as_view(), name="profile"),
]