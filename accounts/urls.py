from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("", views.SignupAPIView.as_view(), name="signup"),
    path("login/", views.LoginAPIView.as_view(), name="login"),
]