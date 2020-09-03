from django import forms
from products.models import Product, Category, Product_Size_Color, Size, Color, Supplier_Account
from django.db import models
from .models import Supplier_Account
from django.core import validators
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
import re
import bcrypt
from multiupload.fields import MultiFileField, MultiMediaField, MultiImageField


class ProductModelForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'category',
            'brand',
            'name',
            'brand',
            'slug',
            'description',
            'discount',
            'staffRecommended',
        ]


class EditProductForm(forms.ModelForm):
    # Image = MultiMediaField(
    #     min_num=1,
    #     max_num=6,
    #     max_file_size=1024*1024*5,
    #     media_type='image'
    # )
    class Meta:
        model = Product_Size_Color
        fields = [
            'price',
            'quantity',

        ]


class Product_Size_ColorModelForm(forms.ModelForm):
    Image = MultiMediaField(
        min_num=1,
        max_num=6,
        max_file_size=1024*1024*5,
        media_type='image'
    )

    class Meta:
        model = Product_Size_Color
        fields = [
            'id',
            'color',
            'size',
            'quantity',
            'price'
        ]


class Supplier_AccountModelForm(forms.ModelForm):
    password = forms.CharField(
        min_length=8, label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        min_length=8, label='Confirm Password', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=200)

    class Meta:
        model = Supplier_Account
        fields = [
            'name',
            'email',
            'phone',
            'company',
            'bank_name',
            'bank_branch',
            'account_owner',
            'account_type',
            'IFSC_code',
            'account_number',
            'PAN_number',
            'GST_number',
            'signature',
            'password',
        ]

    def clean_phone(self):
        phoneno = self.cleaned_data['phone']
        if(len(phoneno) != 10):
            print("wrong phone")
            raise forms.ValidationError("""Enter a valid phone number""")
        return phoneno

    def clean_PAN_number(self):
        pannumber = self.cleaned_data['PAN_number']
        regex = re.compile("[A-Z]{5}[0-9]{4}[A-Z]{1}")
        if(len(pannumber) != 10):
            raise forms.ValidationError(
                """The length of PAN number must be 10""")
        if not regex.match(pannumber):
            raise forms.ValidationError("""Enter a valid pan card number""")
        return pannumber

    def clean_GST_number(self):
        gstnumber = self.cleaned_data['GST_number']
        regex = re.compile(
            "[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}")
        if(len(gstnumber) != 15):
            raise forms.ValidationError(
                """The length of GST number must be 15""")
        if not regex.match(gstnumber):
            raise forms.ValidationError("""Enter a valid GST number""")
        return gstnumber

    def clean_account_number(self):
        accountno = self.cleaned_data['account_number']
        regex = re.compile("[0-9]{9,18}")
        if not regex.match(accountno):
            raise forms.ValidationError("""Enter a valid account number""")
        if Supplier_Account.objects.filter(account_number=accountno).exists():
            raise forms.ValidationError("""Account Number already exist""")
        return accountno

    def clean_IFSC_code(self):
        ifsc = self.cleaned_data['IFSC_code']
        regex = re.compile("^[A-Za-z]{4}0[A-Z0-9a-z]{6}$")
        if not regex.match(ifsc):
            raise forms.ValidationError("""Enter a valid IFSC code""")
        return ifsc

    def clean_email(self):
        emailid = self.cleaned_data['email']
        if emailid and Supplier_Account.objects.filter(email=emailid).exists():
            raise forms.ValidationError(
                """Emailid already exist""", code='email')
        return emailid

    def clean(self):
        cleaned_data = super().clean()
        password_one = self.cleaned_data['password']
        hash_password = bcrypt.hashpw(password_one.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')

        password_two = self.cleaned_data['password2']

        RegexLength = re.compile(r'^\S{8,}$')
        RegexDigit = re.compile(r'\d')
        RegexLower = re.compile(r'[a-z]')
        RegexUpper = re.compile(r'[A-Z]')

        if (password_one != password_two):
            raise forms.ValidationError(
                """Password and Confirm Password did not match""", code='password')
        else:
            if RegexLength.search(password_one) == None or RegexDigit.search(password_one) == None or RegexUpper.search(password_one) == None or RegexLower.search(password_one) == None:
                raise forms.ValidationError(
                    """Enter a strong password""", code='password')

        cleaned_data['password'] = hash_password

        return cleaned_data


class Supplier_LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=100)
    password = forms.CharField(
        min_length=8, label='Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        emailid = cleaned_data['email']
        spassword = cleaned_data['password']

        if emailid and Supplier_Account.objects.filter(email=emailid).exists():
            supplier_obj = Supplier_Account.objects.get(email=emailid)
        else:
            raise ValidationError("""Email Id is not registered..""")

        if not bcrypt.checkpw(spassword.encode('utf-8'), supplier_obj.password.encode('utf-8')):
            raise ValidationError("""Incorrect Password""")

        return cleaned_data


class password_resetForm(forms.Form):
    email = forms.EmailField(max_length=200)

    def clean_email(self):
        cleaned_data = super().clean()

        emailid = cleaned_data['email']

        if emailid and Supplier_Account.objects.filter(email=emailid).exists():
            supplier_obj = Supplier_Account.objects.get(email=emailid)
        else:
            raise ValidationError("""Email Id is not registered..""")

        return cleaned_data


class password_changeForm(forms.Form):
    newpassword = forms.CharField(
        min_length=8, label='Password', widget=forms.PasswordInput)
    newpassword_confirm = forms.CharField(
        min_length=8, label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        password_new = self.cleaned_data['newpassword']
        hash_password_new = bcrypt.hashpw(password_new.encode(
            'utf-8'), bcrypt.gensalt()).decode('utf-8')
        print(hash_password_new)
        password_new_two = self.cleaned_data['newpassword_confirm']

        RegexLength = re.compile(r'^\S{8,}$')
        RegexDigit = re.compile(r'\d')
        RegexLower = re.compile(r'[a-z]')
        RegexUpper = re.compile(r'[A-Z]')

        if (password_new != password_new_two):
            raise forms.ValidationError(
                """Password and Confirm Password did not match""", code='password')
        else:
            if RegexLength.search(password_new) == None or RegexDigit.search(password_new) == None or RegexUpper.search(password_new) == None or RegexLower.search(password_new) == None:
                raise forms.ValidationError(
                    """Enter a strong password""", code='password')

        cleaned_data['newpassword'] = hash_password_new

        return cleaned_data


class supplier_profileForm(forms.ModelForm):

    class Meta:
        model = Supplier_Account
        fields = [
            'name',
            'email',
            'phone',
            'bank_name',
            'bank_branch',
            'account_owner',
            'IFSC_code',
            'account_number'
        ]

    def clean_account_number(self):
        accountno = self.cleaned_data['account_number']
        regex = re.compile("[0-9]{9,18}")
        if not regex.match(accountno):
            raise forms.ValidationError("""Enter a valid account number""")
        if Supplier_Account.objects.filter(account_number=accountno).exists():
            raise forms.ValidationError("""Account Number already exist""")
        return accountno

    def clean_IFSC_code(self):
        ifsc = self.cleaned_data['IFSC_code']
        regex = re.compile("^[A-Za-z]{4}0[A-Z0-9a-z]{6}$")
        if not regex.match(ifsc):
            raise forms.ValidationError("""Enter a valid IFSC code""")
        return ifsc
