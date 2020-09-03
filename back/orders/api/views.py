from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken import views
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from django.contrib import messages
from .serializers import OrderSerializer, OrderItemSerializer
from products.models import Product_Size_Color, Product_Images
from orders.models import Order, OrderItem
from profiles.models import Customer_Profile
from rest_framework.permissions import AllowAny, IsAuthenticated
from cart.models import Cart, CartItem
from rest_framework.views import APIView
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django_email_verification import sendConfirm
from django.core.mail import EmailMessage
from payments.views import back

# from .tasks import order_created
'''
class CartItemViewSet(mixins.ListModelMixin,viewsets.generics):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
'''

class OrderList(APIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "orders/orderlist.html"

    def get(self, request, format=None):
        user = request.user
        if request.user.is_staff:
            orders = Order.objects.all()
        else:
            orders = Order.objects.filter(user=user)
        serializer = OrderSerializer(orders, many=True)
        return Response({'orders': orders})


'''
class OrderViewSet(mixins.CreateModelMixin,mixins.ListModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        if self.request.user.is_staff:
            return Order.objects.all()
        else:
            return Order.objects.filter(user=self.request.user)
    permission_classes = [IsAuthenticated, ]
    serializer_class = OrderSerializer

    def create(self,request):
        cart=Cart.objects.filter(owner=request.user).first()
        cartitems=CartItem.objects.filter(cart=cart)
        order=OrderSerializer(data=request.data,context={'request': request,'cartitems':cartitems})
        if order.is_valid():
            order.save()
            for item in cartitems:
                item.delete()
            #print(order.data)
            return Response(order.data, status=status.HTTP_201_CREATED)
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)
#https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-create-perform-create
'''
# https://resources.oreilly.com/examples/9781784391911/blob/master/Django_By_Example_Code/Chapter%208/myshop/orders/views.py



class OrderDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = Order
    template_name = "orders/detail.html"

    def get(self, request, pk):
        order = Order.objects.filter(user=request.user, pk=pk).first()
        serializer = OrderSerializer(order)
        queryset = OrderItem.objects.filter(order=order)
        order_items = []
        for query in queryset:
            img = Product_Images.objects.filter(
                product_size_color=query.item)[0]
            order_items.append((query, img))
        total = []
        for item in queryset:
            total.append(item.get_final_price())
        return Response({'orderitems': order_items, 'order': order, 'total': total})


class OrderCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class=OrderSerializer
    template_name = "orders/checkout.html"
    style = {'template_pack': 'rest_framework/vertical/'}
    def get(self,request):
        
        customer=Customer_Profile.objects.filter(customer=request.user).first()
        usercart=Cart.objects.get(owner=request.user)
        items = CartItem.objects.filter(cart=usercart)
        data=[]
        for item in items:
            data.append(item.id)
        request.session['items']=data
        print(request.session['items'])
        for item in items:
            item_id = []
            if item.quantity > item.item.quantity:
                print("item is less")
                item_id.append(item.id)
                messages.info(request, 'Quantity for '+ item.item.product.name + ' not available')
                del request.session['items']
                return redirect('cart')
            elif (customer.firstname and customer.phone_number):
                serializer=OrderSerializer()
                return Response({'serializer': serializer,'customer': customer ,'style': self.style})
            else:
                del request.session['items']
                return render(request,'orders/warning.html')



'''
    def post(self,request):
        cart=Cart.objects.filter(owner=request.user).first()
        cartitems=CartItem.objects.filter(cart=cart)
        print(request.data)
        if(request.data['address.id']):
            order=OrderSerializer(data=request.data,context={'request': request,'cartitems':cartitems,'address_id':request.data['address.id']})
            print(request.POST)
        else:
            order=OrderSerializer(data=request.data,context={'request': request,'cartitems':cartitems})
            print(request.POST)
        if order.is_valid():
            print('##############################################')
            order.save()
            # for item in cartitems:
            #    item.delete()
            #print(order.data)
            return redirect('orderdetail',pk=order.data['id'])
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)
'''
'''
    def post(self,request):
        cart=Cart.objects.filter(owner=request.user).first()
        cartitems=CartItem.objects.flter(cart=cart)
        order=OrderSerializer(data=request.data,context={'request': request,'cartitems':cartitems})
        if order.is_valid():
            print('##############################################')
            order.save()
            # for item in cartitems:
            #    item.delete()
            #print(order.data)
            return redirect('orderdetail',pk=order.data['id'])
        return Response(order.errors, status=status.HTTP_400_BAD_REQUEST)
'''


def nextfn(request):
    address_exists = request.POST.get('address.id', False)
    print(address_exists)
    if(address_exists):
        request.session['id'] = request.POST['address.id']
        request.session['locality'] = request.POST['address.locality']
        request.session['landmark'] = request.POST['address.landmark']
        request.session['district'] = request.POST['address.district']
        request.session['state'] = request.POST['address.state']
        request.session['pincode'] = request.POST['address.pincode']        
    else:
        request.session['locality'] = request.POST['address.locality']
        print(request.session['locality'])
        request.session['landmark'] = request.POST['address.landmark']
        request.session['district'] = request.POST['address.district']
        request.session['state'] = request.POST['address.state']
        request.session['pincode'] = request.POST['address.pincode']
    if(request.POST['payment.method']=='COD'):
        print(request.POST['payment.method'])
        request.session['txnid'] = 'COD'
        return redirect(back)
    else:
        return redirect('payment')