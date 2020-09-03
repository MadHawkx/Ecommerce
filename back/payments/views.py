from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
import logging
import traceback
from cart.models import Cart, CartItem
import payments.constants as constants
import payments.config as config
import hashlib
import requests
from random import randint
from django.views.decorators.csrf import csrf_exempt
from profiles.models import Customer_Profile, Address
from orders.models import Order, OrderItem
from django.template.loader import render_to_string
from django_email_verification import sendConfirm
from django.core.mail import EmailMessage
from cart.api.views import CartDetail
from .models import Payment

def payment(request):
    user = request.user
    email = user.email
    profile = Customer_Profile.objects.get(customer=user)
    firstname = profile.firstname
    usercart = Cart.objects.get(owner=request.user)
    items = CartItem.objects.filter(cart=usercart)
    item_id = []
    for item in items:
        if item.quantity > item.item.quantity:
            print("item is less")
            item_id.append(item.id)
            messages.info(request, 'Quantity for ' +
                          item.item.product.name + ' not available')
    if len(item_id) > 0:
        return redirect('cart')
    temp_total=0
    for i in request.session['items']:
        print(int(i))
        temp=CartItem.objects.filter(id=int(i))
        for item in temp:
            temp_total+=item.total()
    print(temp_total)
    amount = float(temp_total)
    phone_number = profile.phone_number
    data = {}
    txnid = get_transaction_id()
    hash_ = generate_hash(request, txnid, firstname, email, amount)
    print(hash_)
    hash_string = get_hash_string(request, txnid, firstname, email, amount)
    # use constants file to store constant values.
    # use test URL for testing
    data["action"] = constants.PAYMENT_URL_TEST
    data["amount"] = float(temp_total)
    data["productinfo"] = constants.PAID_FEE_PRODUCT_INFO
    data["key"] = config.KEY
    data["txnid"] = txnid
    request.session['txnid'] = txnid
    data["hash"] = hash_
    data["hash_string"] = hash_string
    data["firstname"] = firstname
    data["email"] = email
    data["phone_number"] = phone_number
    data["service_provider"] = constants.SERVICE_PROVIDER
    data["furl"] = 'http://127.0.0.1:8000/payment/failure/'
    data["surl"] = 'http://localhost:8000/payment/success/'
    '''
    data['udf1'] = request.session['locality']
    data['email']=request.user.email
    data['udf2'] = request.session['landmark']
    data['udf3'] = request.session['district']
    data['udf4'] = request.session['state']
    data['udf5'] = request.session['pincode']
    '''
    print('$$$$$$$$$$$$$$$$$$$$$$')
    return render(request, "payments/payment_form.html", data)

# generate the hash


def generate_hash(request, txnid, firstname, email, amount):
    try:
        # get keys and SALT from dashboard once account is created.
        # hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = get_hash_string(request, txnid, firstname, email, amount)
        generated_hash = hashlib.sha512(
            hash_string.encode('utf-8')).hexdigest().lower()
        return generated_hash
    except Exception as e:
        # log the error here.
        logging.getLogger("error_logger").error(traceback.format_exc())
        return None


# create hash string using all the fields
def get_hash_string(request, txnid, firstname, email, amount):
    hash_string = config.KEY+"|"+txnid+"|" + \
        str(float(amount))+"|"+constants.PAID_FEE_PRODUCT_INFO+"|"
    hash_string += firstname+"|"+email+"|"
    hash_string += "||||||||||"+config.SALT

    return hash_string


# generate a random transaction Id.
def get_transaction_id():
    hash_object = hashlib.sha256(str(randint(0, 9999)).encode("utf-8"))
    # take approprite length
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid


# no csrf token require to go to Success page.
# This page displays the success/confirmation message to user indicating the completion of transaction.


def back(request):
    address_exists = request.session.get('id', False)
    print(address_exists)
    if(address_exists):
        locality = request.session['locality']
        landmark = request.session['landmark']
        district = request.session['district']
        state = request.session['state']
        pincode = request.session['pincode']
        ad = Address.objects.get(id=request.session.get('id'))
        del request.session['id']
    else:
        locality = request.session['locality']
        landmark = request.session['landmark']
        district = request.session['district']
        state = request.session['state']
        pincode = request.session['pincode']
        ad = Address.objects.create(
            locality=locality, landmark=landmark, district=district, state=state, pincode=pincode)
        ad.save()
    print(locality, landmark, district, state, pincode)
    print(request.user)
    order = Order.objects.create(user=request.user, address=ad)
    order.save()
    usercart = Cart.objects.get(owner=request.user)
    cartitems = CartItem.objects.filter(cart=usercart)

    for i in request.session['items']:
        temp=CartItem.objects.filter(id=int(i))
        print(temp)
        for item in temp:
            if item.quantity < item.item.quantity:
                print("quant is less")
                OrderItem.objects.create(order=order, item=item.item, quantity=item.quantity,
                                         price=item.item.price, discount=item.item.product.discount)
                # supplier = item.item.product.supplier.email
                # mail_subject = 'Product ordered'
                # message = render_to_string('orders/product_ordered.html', {
                #     'user': item.item.product.supplier,
                #     'item': item
                # })
                # email = EmailMessage(
                #     mail_subject, message, to=[supplier]
                # )
                # email.send()
                #Uncomment and enter YOUR WOrking Email with password in back/settings.py
                item.item.quantity -= item.quantity
                item.item.save()
                # item.delete()
            else:
                messages.info(
                    request, 'Out of stock products remain in the cart and those are not included in order')
                return redirect('cart')
        for item in cartitems:
            if item in temp:
                usercart.total-=item.item.price
                usercart.number_of_items-=item.quantity
                item.delete()
    order.total = order.get_total_cost()
    payment=Payment.objects.get(txnid=request.session['txnid'])
    order.payment = request.session['txnid']
    order.save()
    payment.porder=order
    payment.save()
    usercart.save()
    orderitems = OrderItem.objects.filter(order=order)
    # usermail = request.user.email
    # mail_subject = 'Order Placed'
    # message = render_to_string('orders/order_placed.html', {
    #     'user': request.user,
    #     'orderitems': orderitems,
    #     'order': order,
    # })
    # email = EmailMessage(
    #     mail_subject, message, to=[usermail]
    # )
    # email.send()UNCOMMENT AND ENTER YOUR MAIL

    del request.session['items']
   # order.payment=request.session['txnid']
    if request.session['txnid'] == 'COD':
        return HttpResponse('Your order is placed..\nCheck your mail for all the details\n')
    else:
        return redirect("orderlist")


@csrf_exempt
def success(request):
    data = request.POST
    print(data)
    print('##')
    '''
    <QueryDict: {'isConsentPayment': ['0'], 'mihpayid': ['9083970533'], 'mode': ['CC'], 'status': ['success'], 'unmappedstatus': ['captured'], 'key': ['
lVt82uZr'], 'txnid': ['061b4fe85b47a13e1887f386477e0e0d'], 'amount': ['10000.00'], 'addedon': ['2020-08-14 22:03:01'], 'productinfo': ['Message show
ing product details.'], 'firstname': ['Divyam'], 'lastname': [''], 'address1': [''], 'address2': [''], 'city': [''], 'state': [''], 'country': [''],
 'zipcode': [''], 'email': [''], 'phone': ['123456789'], 'udf1': [''], 'udf2': [''], 'udf3': [''], 'udf4': [''], 'udf5': [''], 'udf6': [''], 'udf7'
: [''], 'udf8': [''], 'udf9': [''], 'udf10': [''], 'hash': ['137a3d50db97cc7895567d8625304fa0b9521f9db8acaf8615dfe782b0f087e979e0d027c834cf474aa116d
9b338636bcd2f0268f1889ad00ba14eaf711163d3'], 'field1': ['291610405015'], 'field2': ['443954'], 'field3': ['446255233669809'], 'field4': ['SjFTZmJHT0
dpMjZwaFhRUEJSMHY='], 'field5': ['05'], 'field6': [''], 'field7': ['AUTHPOSITIVE'], 'field8': [''], 'field9': [''], 'giftCardIssued': ['true'], 'PG_
TYPE': ['HDFCPG'], 'encryptedPaymentId': ['30B1A5574019417CEA3B0478A0E80102'], 'bank_ref_num': ['446255233669809'], 'bankcode': ['VISA'], 'error': [
'E000'], 'error_Message': ['No Error'], 'name_on_card': ['divyam'], 'cardnum': ['401200XXXXXX1112'], 'cardhash': ['This field is no longer supported
 in postback params.'], 'amount_split': ['{"PAYU":"10000.00"}'], 'payuMoneyId': ['250440967'], 'discount': ['0.00'], 'net_amount_debit': ['10000']}>
 '''
   # session=Session.objects.create(pk=data['txnid'])
   # session.payuid=data['PayuMoneyId']
    payment=Payment.objects.create(
    txnid=data['txnid'],payuMoneyId=data['payuMoneyId'],mihpayid=data['mihpayid'],amount=data['amount']
    )
    payment.save()
    return redirect('success-redirect')


@csrf_exempt
def failure(request):
    data = request.POST
    print(data)
    return HttpResponseRedirect(reverse(payment_failure))


'''
from payu.gateway import refund_transaction
from payu.gateway import verify_payment
def refund(request,pk):
    response = verify_payment(pk)
    mpid=response.transaction_details.mihpayid
    amount=response.transaction_details.net_amount
    response = refund_transaction(mpid,amount)
    return response
'''

