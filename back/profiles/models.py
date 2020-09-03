from django.db import models
from accounts.models import User
from django.core.exceptions import ValidationError


def validate_digit_length(phone):
    if not (phone.isdigit() and len(phone) == 10):
        raise ValidationError('%(phone)s must be 10 digits',
                              params={'phone': phone},)


class Card_Detail(models.Model):
    card_number = models.IntegerField()
    cvv = models.IntegerField()
    exp_date = models.DateField()


class Address(models.Model):
    locality = models.CharField(max_length=250)
    landmark = models.CharField(max_length=250, blank=True, null=True)
    district = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=10)

    def clean_pincode(self):
        pin = self.cleaned_data['pincode']
        if(len(pin) != 6):
            print("wrong pincode")
            raise forms.ValidationError("""Enter a valid pincode""")
        return pin

    def __str__(self):
        return (str(self.locality)+", "+str(self.landmark)+", "+str(self.district)+", "+str(self.state)+", "+str(self.pincode))


class Customer_Profile(models.Model):
    customer = models.OneToOneField(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=50, blank=True, null=True)
    lastname = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(verbose_name="Phone number", max_length=10,
                                    validators=[validate_digit_length], blank=True, null=True)
    address = models.ManyToManyField(Address, blank=True)
    cards = models.ManyToManyField(Card_Detail, blank=True)
    phone_verification = models.BooleanField(default=False)

    def __str__(self):
        return str(self.customer.email)

    def clean(self):
        if not (self.phone_number.isdigit() and len(self.phone_number) == 10):
            raise ValidationError('%(phone)s must be 10 digits', params={
                                  'phone': self.phone_number},)
