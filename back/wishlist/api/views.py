from products.models import Product
from .serializers import *
from rest_framework.authtoken import views
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.decorators import api_view, authentication_classes
from rest_framework import mixins
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import redirect


class WishlistList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'wishlist/wishlists.html'
    authentication_classes = [SessionAuthentication, BasicAuthentication]

    def get(self, request):
        queryset = Wishlist.objects.filter(owner=request.user)
        return Response({'wishlists': queryset})


class WishlistCreate(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "wishlist/create.html"
    style = {'template_pack': 'rest_framework/vertical/'}
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(owner=user)

    def get(self, request):
        serializer = WishlistSerializer
        return Response({'serializer': serializer, 'style': self.style})

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            wishlist = Wishlist.objects.create()
            '''
            if 'id' in request.data:
                product=Product.objects.get(id=request.data['id'])
                wishlist.products.add(product)
            '''
            wishlist.owner = request.user
            wishlist.name = request.data['name']
            wishlist.save()
            return redirect('wishlistlist')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WishlistDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "wishlist/detail.html"
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    style = {'template_pack': 'rest_framework/vertical/'}
    serializer_class = WishlistSerializer

    def get(self, request, pk):
        user = request.user
        wishlist = Wishlist.objects.get(owner=user, id=pk)
        serializer = WishlistSerializer(wishlist)
        products = wishlist.products.all()
        return Response({'serializer': serializer, 'style': self.style, 'products': products, 'wishlist': wishlist})

    def post(self, request, pk=None):
        wishlist = Wishlist.objects.get(owner=request.user, id=pk)
        print(pk)
        try:
            name = request.data['name']
        except Exception as e:
            print(e)
            return Response({'status': 'fail'})
        if name and len(name) < 20:
            wishlist.name = name
            wishlist.save()
        else:
            return Response({'status': 'fail.name too long'})
        serializer = WishlistSerializer(wishlist)
        return redirect('wishlistdetail', pk=pk)


class WishlistDelete(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = WishlistSerializer

    def get(self, request, pk):
        user = request.user
        wishlist = Wishlist.objects.get(owner=user, id=pk)
        for each in wishlist.products.all():
            wishlist.products.remove(each)
        wishlist.delete()
        return redirect('wishlistlist')


@api_view(['POST', 'PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def add_to_wishlist(request, pk=None):
    wishlist = Wishlist.objects.get(owner=request.user, id=pk)
    print(request.data)
    print("########################")
    try:
        product = Product.objects.get(
            id=request.data['id']
        )
    except Exception as e:
        print(e)
        return Response({'status': 'fail'})
    # print(quantity)

    wishlist.products.add(product)
    wishlist.count = Wishlist.objects.filter(owner=request.user).count()
    wishlist.save()
    serializer = WishlistSerializer(wishlist)
    return Response(serializer.data)


@api_view(['POST', 'PUT'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
def remove_from_wishlist(request, pk):
    wishlist = Wishlist.objects.get(owner=request.user, id=pk)
    print(request.data)
    print("########################")
    try:
        product = Product.objects.get(
            pk=request.data['id']
        )
    except Exception as e:
        print(e)
        return Response({'status': 'fail'})

    wishlist.products.remove(product)
    wishlist.count = Wishlist.objects.filter(owner=request.user).count() - 1
    wishlist.save()
    # return the updated cart to indicate success
    serializer = WishlistSerializer(wishlist)
    return Response(serializer.data)


class WishlistEdit(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "wishlist/edit.html"
    style = {'template_pack': 'rest_framework/vertical/'}
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    serializer_class = WishlistSerializer

    def get_queryset(self):
        user = self.request.user
        return Wishlist.objects.filter(owner=user)

    def get(self, request, pk):
        wishlist = Wishlist.objects.get(owner=request.user, id=pk)
        serializer = WishlistSerializer(wishlist)
        return Response({'serializer': serializer, 'style': self.style, 'wishlist': wishlist})
