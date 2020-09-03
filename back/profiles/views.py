from .models import Customer_Profile, Address, Card_Detail
from accounts.models import User
from .serializers import CustomerProfileSerializer, AddressSerializer, CardDetailSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import redirect
from twilio.rest import Client
from random import randint
from django.contrib import messages
from orders.models import Order


class CustomerProfileDetail(APIView):
    """
    Retrieve, update or delete a CustomerProfile instance.
    """
    queryset = Customer_Profile.objects.all()
    serializer_class = CustomerProfileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/detail.html"

    def get_object(self, request):
        try:
            customer = request.user
            return Customer_Profile.objects.get(customer=customer)
        except Customer_Profile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        print('%%%%%%%%%%%%%')
        customerprofile = self.get_object(request)
        serializer = CustomerProfileSerializer(customerprofile)
        return Response({'profile': customerprofile})


class CustomerProfileUpdate(APIView):
    queryset = Customer_Profile.objects.all()
    serializer_class = CustomerProfileSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/index.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get_object(self, request):
        try:
            customer = request.user
            return Customer_Profile.objects.get(customer=customer)
        except Customer_Profile.DoesNotExist:
            raise Http404

    def get(self, request, format=None):
        print('%%%%%%%%%%%%%')
        customerprofile = self.get_object(request)
        serializer = CustomerProfileSerializer(customerprofile)
        return Response({'serializer': serializer, 'style': self.style, 'profile': customerprofile})

    def post(self, request, format=None):
        print('##############')
        customerprofile = self.get_object(request)
        serializer = CustomerProfileSerializer(
            customerprofile, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('profile_detail')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerAddressList(APIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/addresslist.html"

    def get(self, request, format=None):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        serializer = AddressSerializer(
            customerprofile.address.all(), many=True)
        return Response({'address': customerprofile.address.all()})


class CustomerAddressCreate(APIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/addresscreate.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = AddressSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request, format=None):
        serializer = AddressSerializer(data=request.data)
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        if serializer.is_valid():
            address = Address(**serializer.data)
            address.save()
            customerprofile.address.add(address)
            return redirect('addresslist')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerAddressDetail(APIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/addressedit.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request, pk):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        serializer = AddressSerializer(customerprofile.address.get(id=pk))
        return Response({'serializer': serializer, 'style': self.style, 'address': customerprofile.address.get(id=pk)})

    def post(self, request, pk, format=None):
        address = Address.objects.get(id=pk)
        serializer = AddressSerializer(address, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('addresslist')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerAddressDelete(APIView):
    def get(self, request, pk):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        addresses = customerprofile.address.all().values()
        obj = customerprofile.address.get(id=pk)
        customerprofile.address.remove(obj)
        obj = Address.objects.get(id=pk)
        order_objs = Order.objects.filter(address=obj)
        if len(order_objs) == 0:
            obj.delete()
        # customerprofile = self.get_object(request)
        # serializer = CustomerProfileSerializer(customerprofile)
        # return Response(serializer.data)
        return redirect('addresslist')


class CustomerCardList(APIView):
    queryset = Address.objects.all()
    serializer_class = CardDetailSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/cardlist.html"

    def get(self, request, format=None):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        serializer = CardDetailSerializer(
            customerprofile.cards.all(), many=True)
        return Response({'cards': customerprofile.cards.all()})


class CustomerCardCreate(APIView):
    queryset = Card_Detail.objects.all()
    serializer_class = CardDetailSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/cardcreate.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request):
        serializer = CardDetailSerializer()
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request, format=None):
        print('$$$$$$$$$$$$$$$$$$$$$$$$')
        serializer = CardDetailSerializer(data=request.data)
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        if serializer.is_valid():
            card = Card_Detail(**serializer.data)
            card.save()
            customerprofile.cards.add(card)
            return redirect('cardlist')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerCardDetail(APIView):
    queryset = Card_Detail.objects.all()
    serializer_class = CardDetailSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/cardedit.html"
    style = {'template_pack': 'rest_framework/vertical/'}

    def get(self, request, pk):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        serializer = CardDetailSerializer(customerprofile.cards.get(id=pk))
        return Response({'serializer': serializer, 'style': self.style, 'card': customerprofile.cards.get(id=pk)})

    def post(self, request, pk, format=None):
        print('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
        cards = Card_Detail.objects.get(id=pk)
        serializer = CardDetailSerializer(cards, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return redirect('cardlist')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerCardDelete(APIView):
    def get(self, request, pk):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        cards = customerprofile.cards.all().values()
        obj = customerprofile.cards.get(id=pk)
        customerprofile.cards.remove(obj)
        obj = Card_Detail.objects.get(id=pk)
        obj.delete()

       # customerprofile = self.get_object(request)
       # serializer = CustomerProfileSerializer(customerprofile)
       # return Response(serializer.data)
        return redirect('cardlist')


class PhoneVerification(APIView):
    queryset = Customer_Profile.objects.all()
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "profiles/phoneverification.html"
    serializer_class = CustomerProfileSerializer

    def get(self, request):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        if customerprofile.phone_verification:
            messages.error(request, 'Phone Already Verified')
            return redirect('profile_detail')
        else:
            phone = customerprofile.phone_number
            serializer = CustomerProfileSerializer(customerprofile)
            # key=send_otp(key)
            if phone:
                phone_num = str(phone)
                request.session['otp'] = send_otp(phone_num)
                code = str(request.session['otp'])
                account_sid = ''#add
                auth_token = ''#add
                client = Client(account_sid, auth_token)

                message = client.messages.create(
                    body=code+' is your OTP for YIF phone verification',
                    from_='+',
                    to='+91'#add with +91
                )
                print(message.sid)
            #     else:
            #         return({'status':False,'detail':'otp not sent. Error'})

            # else:
            #     return({'status':False, 'detail':'Phone Number Not Given'})
            print(customerprofile.phone_verification)
            return Response({'profile': customerprofile, 'key': request.session['otp']})

    def post(self, request, format=None):
        user = request.user
        customerprofile = Customer_Profile.objects.get(customer=user)
        phone = customerprofile.phone_number
        otp = request.session['otp']
        key = request.POST.get('otp', False)
        print(otp)
        print(key)
        print(request.POST)
        if str(otp) == key:
            customerprofile.phone_verification = True
            customerprofile.save()
            return redirect('profile_detail')
        else:
            messages.error(request, 'The OTP You Entered Was Wrong')
            return redirect('profile_detail')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def send_otp(phone):
    if phone:
        key = randint(999, 9999)
        return key
