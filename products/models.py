from django.db import models
from django.conf import settings

# Create your models here.
class Product(models.Model):
    titel=models.CharField(max_length=10)
    content=models.TextField
    price=models.DecimalField(max_digits=10,decimal_places=2)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="products")

    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_products")

    def __str__(self):
        return self.title