from django.shortcuts import render, redirect
from cart.models import *
from products.models import Product_Size_Color, Product_Images
from .serializers import *
from rest_framework.authtoken import views
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework import mixins, generics
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer


class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer


class CartList(mixins.ListModelMixin, generics.GenericAPIView):
    def get_queryset(self, request):
        if request.user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(owner=request.user).first()

    serializer_class = CartSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CartDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = Cart
    template_name = "cart/index.html"

    def get(self, request, format=None):
        cart = Cart.objects.filter(owner=request.user).first()
        serializer = CartSerializer(cart)
        queryset = CartItem.objects.filter(cart=cart)
        cart_items = []
        for query in queryset:
            img = Product_Images.objects.filter(
                product_size_color=query.item)[0]
            cart_items.append((query, img))
        return Response({'items': cart_items, 'cart': cart})


@api_view(['POST', 'PUT'])
def add_to_cart(request):
    cart = Cart.objects.get(owner=request.user)
    print("########################")
    try:
        product = Product_Size_Color.objects.get(
            id=request.data['id']
        )
        # print(product)
        quantity = int(request.data['quantity'])
    except Exception as e:
        print(e)
        return Response({'status': 'fail'})
    items = CartItem.objects.filter(cart=cart)

    # print(quantity)
    # Disallow adding to cart if available inventory is not enough
    if product.quantity - quantity < 0:
        print("There is no more product available")
        return Response({'status': 'fail'})

    existing_cart_item = CartItem.objects.filter(
        cart=cart, item=product).first()
    # before creating a new cart item check if it is in the cart already
    # and if yes increase the quantity of that item
    if existing_cart_item:
        if existing_cart_item.quantity + quantity > product.quantity:
            print("There is no more product available")
            return Response({'status': 'fail'})
        existing_cart_item.quantity += quantity
        existing_cart_item.save()
    else:
        new_cart_item = CartItem(cart=cart, item=product, quantity=quantity)
        new_cart_item.save()

    # return the updated cart to indicate success
    total = 0
    count = 0
    items = CartItem.objects.filter(cart=cart)
    for i in items:
        total += i.total()
        count += i.quantity

    cart.total = total
    cart.number_of_items = count
    cart.save()
    serializer = CartSerializer(cart)
    return Response(serializer.data)


@api_view(['POST', 'PUT'])
def remove_from_cart(request):
    cart = Cart.objects.filter(owner=request.user).first()
    try:
        cart_item = CartItem.objects.get(cart=cart, id=request.data['id'])
        print(cart_item)
        product = Product_Size_Color.objects.get(
            pk=cart_item.item.id
        )
    except Exception as e:
        print(e)
        return Response({'status': 'fail'})

    # if removing an item where the quantity is 1, remove the cart item
    # completely otherwise decrease the quantity of the cart item
    cart_item.delete()
    total = 0
    count = 0
    items = CartItem.objects.filter(cart=cart)
    for i in items:
        total += i.total()
        count += i.quantity

    cart.total = total
    cart.number_of_items = count
    cart.save()
    # return the updated cart to indicate success
    serializer = CartSerializer(cart)
    cartitems = CartItem.objects.filter(cart=cart)
    return Response(serializer.data)


@api_view(['POST', 'PUT'])
def update_cart(request):
    cart = Cart.objects.filter(owner=request.user).first()
    try:
        cart_item = CartItem.objects.get(cart=cart, id=request.data['id'])
        quantity = int(request.data['quantity'])
        print(cart_item)
        product = Product_Size_Color.objects.get(
            pk=cart_item.item.id
        )
    except Exception as e:
        print(e)
        return Response({'status': 'fail'})

    # if removing an item where the quantity is 1, remove the cart item
    # completely otherwise decrease the quantity of the cart item
    if cart_item.item.quantity < quantity:
        print("Not Available")
        return Response({'status': 'fail'})

    cart_item.quantity = quantity
    cart_item.save()
    total = 0
    count = 0
    items = CartItem.objects.filter(cart=cart)
    for i in items:
        total += i.total()
        count += i.quantity

    cart.total = total
    cart.number_of_items = count
    cart.save()
    # return the updated cart to indicate success
    serializer = CartSerializer(cart)
    return Response(serializer.data)


'''
def  total_cost(quantity, price):
    return quantity*price
class CartItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows cart items to be viewed or edited.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer

class CartViewSet(mixins.ListModelMixin,mixins.UpdateModelMixin,mixins.RetrieveModelMixin,viewsets.GenericViewSet):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(owner=user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True,methods=['Post','Put'])
    def add_to_cart(self, request, pk=None):
        cart = self.get_object()
        print(request.data)
        print("########################")
        try:
            product = Product_Size_Color.objects.get(
                id=request.data['id']
            )
            #print(product)
            quantity = int(request.data['quantity'])
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})
        # print(quantity)
        # Disallow adding to cart if available inventory is not enough
        if  product.quantity - quantity <0  :
            print ("There is no more product available")
            return Response({'status': 'fail'})

        existing_cart_item = CartItem.objects.filter(cart=cart,item=product).first()
        # before creating a new cart item check if it is in the cart already
        # and if yes increase the quantity of that item
        if existing_cart_item:
            if  existing_cart_item.quantity +quantity>product.quantity :
                print ("There is no more product available")
                return Response({'status': 'fail'})
            existing_cart_item.quantity += quantity
            existing_cart_item.save()
        else:
            new_cart_item = CartItem(cart=cart, item=product, quantity=quantity)
            new_cart_item.save()

        # return the updated cart to indicate success
        total=0
        count=0
        items=CartItem.objects.filter(cart=cart)
        for i in items:
            total+=i.total()
            count+=i.quantity

        cart.total=total
        cart.number_of_items=count
        cart.save()
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True,methods=['Post','Put'])
    def remove_from_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            cart_item=CartItem.objects.get(cart=cart,id=request.data['id'])
            print(cart_item)
            product = Product_Size_Color.objects.get(
                pk=cart_item.item.id
            )
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})


        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        cart_item.delete()
        total=0
        count=0
        items=CartItem.objects.filter(cart=cart)
        for i in items:
            total+=i.total()
            count+=i.quantity

        cart.total=total
        cart.number_of_items=count
        cart.save()
        # return the updated cart to indicate success
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @action(detail=True,methods=['Post','Put'])
    def update_cart(self, request, pk=None):
        cart = self.get_object()
        try:
            cart_item=CartItem.objects.get(cart=cart,id=request.data['id'])
            quantity=int(request.data['quantity'])
            print(cart_item)
            product = Product_Size_Color.objects.get(
                pk=cart_item.item.id
            )
        except Exception as e:
            print (e)
            return Response({'status': 'fail'})


        # if removing an item where the quantity is 1, remove the cart item
        # completely otherwise decrease the quantity of the cart item
        if cart_item.item.quantity<quantity:
            print("Not Available")
            return Response({'status': 'fail'})

        cart_item.quantity=quantity
        cart_item.save()
        total=0
        count=0
        items=CartItem.objects.filter(cart=cart)
        for i in items:
            total+=i.total()
            count+=i.quantity

        cart.total=total
        cart.number_of_items=count
        cart.save()
        # return the updated cart to indicate success
        serializer = CartSerializer(cart)
        return Response(serializer.data)

#https://stackoverflow.com/questions/43456959/how-get-context-react-using-django
# https://www.django-rest-framework.org/api-guide/requests/
#X-CSRFToken: iSnthA2zdz5Wwdtg850aUZbFLQEkS7l61qdoHOuN04V7DOIVwJNGJK3xQQWBjnmC

# X-CSRFToken : M6dhlPSErqdZbl0h42uJq7HwW8VlLPb4qQnGzBGbVQH5TJQ9zPI5bKMpwo4Ts2Ls
# gg@mailscv.com
# asdf@123

'''
