from django.db import models
from accounts.models import User
from products.models import Product
# Create your models here.


class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')
    userrating = models.IntegerField(
        choices=list(zip(range(1, 6), range(1, 6))))
    detail = models.TextField(blank=True, null=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # image=models.ImageField(upload_to='reviews',blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.user.email

# https://github.com/zinmyoswe/React-and-Django-Ecommerce/blob/master/core/models.py
# https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#Uploading_a_file
