# nopep8
from django.utils import timezone
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from allauth.account.signals import user_signed_up, email_confirmed


def validate_digit_length(phone):
    if not (phone.isdigit() and len(phone) == 10):
        raise ValidationError('%(phone)s must be 10 digits',
                              params={'phone': phone},)


class UserManager(BaseUserManager):

    def _create_user(self, email, password, is_staff, is_superuser, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, **extra_fields):
        return self._create_user(email, password, False, False, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        user = self._create_user(email, password, True, True, **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(_('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active status'), default=True)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    def __str__(self):              # __unicode__ on Python 2
        return self.email


# This code is triggered whenever a new user has been created and saved to the database
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    from wishlist.models import Wishlist
    from cart.models import Cart
    from profiles.models import Customer_Profile

    if created:
        Token.objects.create(user=instance)
        Customer_Profile.objects.create(customer=instance)#sudo apt-get remove --auto-remove python-autopep8
        cart = Cart.objects.create(owner=instance)
        wishlist = Wishlist.objects.create(owner=instance, name="wishlist1")


'''
from profiles.models import Customer_Profile
from cart.models import Cart
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        Customer_Profile.objects.create(customer=instance)
        cart=Cart.objects.create(owner=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        cart=Cart.objects.create(owner=instance)
'''
