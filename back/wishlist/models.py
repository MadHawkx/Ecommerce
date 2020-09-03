from django.db import models
from accounts.models import User
from products.models import Product


class Wishlist(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50, editable=True, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return str(self.id)

#  csrftoken=JvhxZr50eaAZhsJHGcBzLskwXyhOlcKwLP2xcn4tKDQygB2VLrPbIIOji646MFO2
