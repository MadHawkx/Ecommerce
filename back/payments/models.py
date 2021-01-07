from django.db import models
from orders.models import Order
# Create your models here.
class Payment(models.Model):
    payuMoneyId=models.CharField(max_length=20)
    txnid=models.CharField(max_length=50)
    mihpayid=models.CharField(max_length=20)
    amount=models.DecimalField(max_digits=9,decimal_places=2,default=0)
    porder=models.OneToOneField(Order,blank=True, null=True, on_delete=models.DO_NOTHING,related_name='porder')
        
