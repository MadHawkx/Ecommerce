from django.shortcuts import render, redirect
from products.models import *
from .models import Supplier_Account
from django.db import connection
from .forms import *
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django_email_verification import sendConfirm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .decorators import is_supplier, is_loggedin
import os
import datetime
from django.utils import timezone
from django.db.models import Q
from django.core.files import File
from django.views.generic import ListView
from django.core.paginator import Paginator
from orders.models import Order, OrderItem
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from .serializers import *
from twilio.rest import Client
from random import randint


@is_loggedin
@is_supplier
def view_history(request, product_id):
    obj = Product_Size_Color.objects.select_related(
        'product__supplier').get(id=product_id)
    if obj.product.supplier.email != request.session['user_email']:
        raise PermissionDenied
    else:
        pro_his_objs = Product_History.objects.filter(product_size_color=obj)
        return render(request, "supplier/display_history.html", {'obj': pro_his_objs})


@is_loggedin
@is_supplier
def add_product(request):
    if request.method == "POST":
        pform = ProductModelForm(request.POST)
        if pform.is_valid():
            obj = pform.save(commit=False)
            obj.supplier = Supplier_Account.objects.get(
                email=request.session['user_email'])
            obj.save()
            pform.save_m2m()
            pro_obj = Product.objects.latest('id')
            return redirect(add_product_specifications, pro_obj.id)
        return redirect(display_product)
    form = ProductModelForm(request.POST or None)
    prods = {
        'form': form
    }
    return render(request, "supplier/addprod.html", {'prods': prods})


@is_loggedin
@is_supplier
def add_product_specifications(request, product_id):
    product_obj = Product.objects.get(id=int(product_id))
    if request.method == "POST":
        if request.POST.get('f1') == 'Save':
            pform = Product_Size_ColorModelForm(request.POST, request.FILES)
            img_list = []
            if pform.is_valid():
                images = pform.cleaned_data['Image']
                del pform.fields['Image']
                obj = pform.save(commit=False)
                obj.product = product_obj
                obj.save()
                psc = Product_Size_Color.objects.latest('id')
                for each in images:
                    Product_Images.objects.create(
                        Image=each, product_size_color=psc)
                return redirect(display_product)
            else:
                prods = {
                    'form': pform
                }
                return render(request, "supplier/prod_spec.html", {'prods': prods})
        elif request.POST.get('f1') == 'Save Add another':
            product_obj = Product.objects.get(id=int(product_id))
            pform = Product_Size_ColorModelForm(request.POST, request.FILES)
            img_list = []
            if pform.is_valid():
                images = pform.cleaned_data['Image']
                del pform.fields['Image']
                obj = pform.save(commit=False)
                obj.product = product_obj
                obj.save()
                psc = Product_Size_Color.objects.latest('id')
                for each in images:
                    Product_Images.objects.create(
                        Image=each, product_size_color=psc)
                return redirect(add_product_specifications, product_id)
            else:
                prods = {
                    'form': pform
                }
                return render(request, "supplier/prod_spec.html", {'prods': prods, 'prod_name': product_obj.name})
    form = Product_Size_ColorModelForm(request.POST or None)
    prods = {
        'form': form
    }
    return render(request, "supplier/prod_spec.html", {'prods': prods, 'prod_name': product_obj.name})


@is_loggedin
@is_supplier
def display_product(request):
    supplier = request.session['user_email']
    product_images = []
    products = Product_Size_Color.objects.prefetch_related('product__category').select_related(
        'product__supplier').filter(product__supplier__email=supplier)
    abc = []
    for pr in products:
        product_image = Product_Images.objects.filter(product_size_color=pr)
        cat = pr.product.category.all()
        abc.append((pr, cat, product_image))
    paginator = Paginator(abc, 1)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    # print(products.query)
    return render(request, "supplier/display_products.html", {'supplier': supplier, 'page_obj': page_obj})


def register_supplier(request):
    if request.method == "POST":
        sform = Supplier_AccountModelForm(request.POST, request.FILES)
        if sform.is_valid():
            del sform.fields['password2']
            obj = sform.save()
            print(sform)
            current_site = get_current_site(request)
            print(current_site.domain)
            # print(obj.query)
            mail_subject = 'Activate your Supplier account.'
            message = render_to_string('supplier/acc_active_email.html', {
                'user': obj,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(obj.pk)),
                'token': account_activation_token.make_token(obj),
            })
            to_email = obj.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
        else:
            sup = {
                'form': sform

            }
            return render(request, "supplier/supplier_register.html", {'sup': sup})
    else:
        form = Supplier_AccountModelForm(request.POST or None)
        sup = {
            'form': form
        }
        errors = ''
        return render(request, "supplier/supplier_register.html", {'sup': sup})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Supplier_Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Supplier_Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_email_active = True
        user.save()
        print("user registered")
        site = get_current_site(request)
        print(site)
        mail_subject = 'Activate the Supplier account.' + user.email
        message = render_to_string('supplier/acc_activate_supplier.html', {
            'user': user,
            'domain': site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = 'YIF.ecommerce@gmail.com'
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()
        print("email sent")
        # return redirect('home')
        request.session['user_email'] = user.email
        return HttpResponse('Thank you for your email confirmation. Go to link http://127.0.0.1:8000/supplier/validate_phone to validate your phone')
    else:
        return HttpResponse('Activation link is invalid!')


def activate_supplier(request, uidb64, token):
    print("request recieved")
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Supplier_Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Supplier_Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and user.is_email_active and user.is_phone_active:
        user.is_approved = True
        user.save()
        return HttpResponse('Your account has been approved. Now you can login your account to add products.')
    else:
        return HttpResponse('Activation link is invalid!')


@is_loggedin
@is_supplier
def supplier_profie(request):
    print("Under Construction")
    return redirect(add_product)


def login_supplier(request):
    if 'user_email' in request.session:
        return redirect('display_prouct')
    if request.method == "POST":
        login_form = Supplier_LoginForm(request.POST)
        if login_form.is_valid():
            print(login_form['email'].value())
            supplier = Supplier_Account.objects.get(
                email=login_form['email'].value())
            if not supplier.is_phone_active:
                request.session['user_email'] = login_form['email'].value()
                return(redirect('validate_phone'))
            if supplier.is_approved:
                request.session['user_email'] = login_form['email'].value()
                request.session['user_role'] = 'supplier'
                return HttpResponse('You are successfully logged in')
            else:
                return HttpResponse('Wait for the admin to approve your application')
        else:
            sup_login = {
                'form': login_form
            }
            return render(request, "supplier/supplier_login.html", {'sup_login': sup_login})

    else:
        form = Supplier_LoginForm(request.POST or None)
        sup_login = {
            'form': form
        }
        errors = ''
        return render(request, "supplier/supplier_login.html", {'sup_login': sup_login})


@is_loggedin
def logout_supplier(request):
    try:
        del request.session['user_email']
        if 'user_role' in request.session:
            del request.session['user_role']
        return HttpResponse('Logged out successfully')
    except:
        return HttpResponse('Some error occured..Try again later')


def password_reset(request):
    if request.method == 'POST':
        emailform = password_resetForm(request.POST)
        if emailform.is_valid():
            user = Supplier_Account.objects.get(
                email=emailform['email'].value())
            site = get_current_site(request)
            mail_subject = 'Change Password.' + user.email
            message = render_to_string('supplier/password_reset_supplier.html', {
                'user': user,
                'domain': site,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = user.email
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Check your mail for further steps')
        else:
            password_form = {
                'form': emailform
            }
            return render(request, "supplier/password_reset.html", {'password_form': password_form})
    else:
        form = password_resetForm(request.POST or None)
        password_form = {
            'form': form
        }
        errors = ''
        return render(request, "supplier/password_reset.html", {'password_form': password_form})


def password_reset_supplier(request, uidb64, token):
    if request.method == 'POST':
        if 'user_email' in request.session:
            password_change_form = password_changeForm(request.POST)
            if password_change_form.is_valid():
                new_pass = password_change_form.cleaned_data['newpassword']
                user = Supplier_Account.objects.get(
                    email=request.session['user_email'])
                user.password = new_pass
                user.save()
                del request.session['user_email']
                if 'user_role' in request.session:
                    del request.session['user_role']
                return HttpResponse('Your password has been changed. Try to login again with new password')
        else:
            return HttpResponse('Something went wrong')
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Supplier_Account.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Supplier_Account.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token) and user.is_email_active:
        request.session['user_email'] = user.email
        form = password_changeForm(request.POST or None)
        password_form = {
            'form': form
        }
        errors = ''
        return render(request, 'supplier/change_password.html', {'password_form': password_form})
    else:
        return HttpResponse('Could not verify your account')


@is_loggedin
@is_supplier
def update_password(request):
    if request.method == 'POST':
        password_change_form = password_changeForm(request.POST)
        if password_change_form.is_valid():
            new_pass = password_change_form.cleaned_data['newpassword']
            user = Supplier_Account.objects.get(
                email=request.session['user_email'])
            user.password = new_pass
            user.save()
            del request.session['user_email']
            del request.session['user_role']
            return HttpResponse('Your password has been changed. Try to login again with new password')
        else:
            return HttpResponse('Something went wrong')
    else:
        form = password_changeForm(request.POST or None)
        password_form = {
            'form': form
        }
        errors = ''
        return render(request, 'supplier/change_password.html', {'password_form': password_form})


@is_loggedin
@is_supplier
def edit_product(request, product_id):
    obj = Product_Size_Color.objects.select_related(
        'product__supplier').get(id=product_id)

    if obj.product.supplier.email != request.session['user_email']:
        raise PermissionDenied
    if obj.status == 'deleted':
        raise PermissionDenied
    if request.method == 'POST':
        edit_product_form = EditProductForm(request.POST, request.FILES)
        if edit_product_form.is_valid():
            Product_History.objects.create(
                product_size_color=obj, price=obj.price, quantity=obj.quantity, datetime=timezone.now())
            psc = Product_Size_Color.objects.get(id=product_id)
            psc.quantity = edit_product_form.cleaned_data['quantity']
            psc.price = edit_product_form.cleaned_data['price']
            psc.status = 'updated'
            psc.save()
            return redirect(display_product)
            # for each in images:
            #     Product_Images.objects.create(Image=each, product_size_color=psc)
        else:
            edit_form = {
                'form': edit_product_form
            }
            return render(request, 'supplier/edit_product.html', {'edit_form': edit_form})
    else:

        edit_form = EditProductForm(instance=obj)
        edit_form = {
            'form': edit_form
        }
        errors = ''
        return render(request, 'supplier/edit_product.html', {'edit_form': edit_form})


@is_loggedin
@is_supplier
def delete_product(request, product_id):
    obj = Product_Size_Color.objects.get(id=product_id)
    if obj.product.supplier.email != request.session['user_email']:
        raise PermissionDenied
    if obj.status == 'deleted':
        raise PermissionDenied
    obj.status = 'deleted'
    obj.save()
    return redirect(display_product)


@is_loggedin
@is_supplier
def ordered_products(request):
    supp = Supplier_Account.objects.get(email=request.session['user_email'])
    obj = OrderItem.objects.filter(item__product__supplier=supp)

    paginator = Paginator(obj, 1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'supplier/ordered_products.html', {'page_obj': page_obj})


def send_otp(phone):
    if phone:
        key = randint(99999, 999999)
        return key


@is_loggedin
def validate_phone(request):
    if request.method == "POST":
        supplier_email = request.session['user_email']
        supplier_profile = Supplier_Account.objects.get(email=supplier_email)
        phone = supplier_profile.phone
        otp = request.session['otp']
        key = request.POST.get('otp', False)
        print(otp)
        print(key)
        print(request.POST)
        if str(otp) == key:
            supplier_profile.is_phone_active = True
            supplier_profile.save()
            request.session['user_role'] = 'supplier'
            return redirect('display_product')
        else:
            messages.error(request, 'The OTP You Entered Was Wrong')
            return Response("Couldn't verify that it's your phone")
            # return redirect('validate_phone')
    supplier_email = request.session['user_email']
    supplier_profile = Supplier_Account.objects.get(email=supplier_email)
    if supplier_profile.is_phone_active:
        request.session['user_role'] = 'supplier'
        return redirect('display_product')
    else:
        phone_num = str(supplier_profile.phone)
        request.session['otp'] = send_otp(phone_num)
        code = str(request.session['otp'])
        account_sid = ''
        auth_token = ''
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            body=code+' is your OTP for YIF supplier phone verification',
            from_='',
            to='+91' + phone_num
            # to=''
        )
        print(message.sid)
        print(supplier_profile.is_phone_active)
        return render(request, "supplier/phoneverification.html")



# @is_loggedin
# @is_supplier
# def supplier_profile(request):
#     if request.method == 'POST':
#         profileform = supplier_profileForm(request.POST, request.FILES)
#         if profileform.is_valid():
#             supplier = Supplier_Account.objects.get(email=request.session['user_email'])
#             supplier.name = profileform.cleaned_data['name']
#             supplier.bank_name = profileform.cleaned_data['bank_name']
#             supplier.bank_branch = profileform.cleaned_data['bank_branch']
#             supplier.account_owner = profileform.cleaned_data['account_owner']
#             supplier.IFSC_code = profileform.cleaned_data['IFSC_code']
#             supplier.account_number = profileform.cleaned_data['account_number']
#             supplier.save()
#             return HttpResponse('Supplier Profile')
#         else:
#             profile_form = {
#                 'form':profileform
#             }
#             return render(request, "supp_profile.html",{'profile_form':profile_form})
#     else:
#         supp = Supplier_Account.objects.get(email=request.session['user_email'])
#         form = supplier_profileForm(instance=supp)

#         profile_form = {
#             'form':form
#         }
#         errors = ''
#         return render(request, "supp_profile.html",{'profile_form':profile_form, 'supplier':supp})
