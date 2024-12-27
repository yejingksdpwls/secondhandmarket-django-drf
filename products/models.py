from django.db import models
from django.conf import settings


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="products/")
    see_count = models.PositiveIntegerField(default=0)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")

    like_user = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="like_products"
    )

    def __str__(self):
        return self.title