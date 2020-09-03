from django.db import models
from accounts.models import User
from products.models import Product, Product_Size_Color


class Cart(models.Model):
    owner = models.OneToOneField(
        User, related_name="cart", on_delete=models.CASCADE, null=True, blank=True)
    number_of_items = models.PositiveIntegerField(default=0)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)+self.owner.email


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cartitem")
    item = models.ForeignKey(Product_Size_Color, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return (str(self.id))

    def total(self):
        return self.quantity * (self.item.price-self.item.product.discount)

    def name(self):
        return self.item.product.name

    def price(self):
        return self.item.price
# https://github.com/beda-software/drf-writable-nested

# https://github.com/jessanettica/simple-shopping-api/blob/master/ecommercesite/shop/models.py
# https://github.com/codingforentrepreneurs/ecommerce-2-api
# https://github.com/zinmyoswe/React-and-Django-Ecommerce/blob/master/core/models.py
# https://github.com/AmirAhrari/django-react-ecommerce/blob/master/orders/models.py
