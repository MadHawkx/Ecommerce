from django.db import models

# Create your models here.


class Supplier_Account(models.Model):
    ACCOUNT_CHOICES = (
        ('savings', 'SAVINGS'),
        ('overdraft', 'OVERDRAFT'),
        ('current', 'CURRENT'),
    )

    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=250)
    phone = models.CharField(max_length=10)
    company = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    bank_branch = models.CharField(max_length=100)
    account_owner = models.CharField(max_length=100)
    IFSC_code = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    account_type = models.CharField(
        max_length=50, choices=ACCOUNT_CHOICES, default='current')
    PAN_number = models.CharField(max_length=10)
    GST_number = models.CharField(max_length=15)
    signature = models.ImageField(upload_to="supplier/signature", blank=True)
    is_email_active = models.BooleanField(default=False)
    is_phone_active = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
