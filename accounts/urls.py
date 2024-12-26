from django.contrib import admin
from django.urls import path
from accounts import views

urlpatterns = [
    path("signup/", views.SignupAPIView.as_view(), name="signup"),
]