from django.contrib import admin
from django.urls import path
from products import views

urlpatterns = [
    path("", views.ProductAPIView.as_view(), name="product-create"),
]
