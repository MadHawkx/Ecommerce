from django.db import models
from products.models import Product_Size_Color
from profiles.models import Address, Card_Detail
from cart.models import Cart
from accounts.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    #ref_code = models.CharField(max_length=20, blank=True, null=True)
    #start_date = models.DateTimeField()
    ordered_date = models.DateTimeField(auto_now_add=True)
    ordered = models.BooleanField(default=False)
    address = models.ForeignKey(
        Address, related_name='address', on_delete=models.DO_NOTHING)
        
    total = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    payment = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        ordering = ('-ordered_date',)

    def __str__(self):
        return self.user.email

    def get_total_cost(self):
        return sum(item.get_final_price() for item in self.orderitems.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name="orderitems", on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Product_Size_Color, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    #coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)

    #shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.SET_NULL)
    #being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    received_date = models.DateTimeField(blank=True, null=True)
    replacement_requested = models.BooleanField(default=False)
    replaced = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.item.product.name}:{self.quantity}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.get_total_item_price() - self.quantity * self.item.product.discount

    def get_final_price(self):
        if self.item.product.discount:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


'''   
    @property
    def is_suspended(self):
        return date.today() < self.end_suspension_date
'''


class Order_Refund(models.Model):
    STATUS_CHOICES = (
        ('default', 'PROCESSING'),
        ('success', 'REFUND_COMPLETED'),
        ('fail', 'REFUND_FAILED'),
    )
    orderitem = models.ForeignKey(
        OrderItem, on_delete=models.DO_NOTHING, blank=True, null=True)
    refund_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default='default')

# import datetime
# import pytz
@receiver(post_save, sender=Order_Refund)
def post_save(sender, instance, created, **kwargs):
    if created:
        mail_subject = 'Refund requested by' + instance.orderitem.order.user.email
        message = render_to_string('orders/refund_mail.html', {
            'domain': site.domain,
            'orderid': instance.orderitem.order.id,
            'orderitem': instance.orderitem,

        })
        to_email = 'YIF.ecommerce@gmail.com'
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()


# https://www.udemy.com/course/the-complete-sql-bootcamp/

# https://docs.djangoproject.com/en/3.1/topics/db/models/https://stackoverflow.com/questions/36719566/identify-the-changed-fields-in-django-post-save-signal
