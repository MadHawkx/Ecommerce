from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.authtoken import views
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductSerializer
from products.models import Product_Size_Color, Category, Product, Product_Images
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import TemplateHTMLRenderer
from wishlist.models import Wishlist
from reviews.models import Reviews
from rest_framework.views import APIView
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from django.core.paginator import Paginator


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


'''
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    # permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["category__title", "name", "description"]

class ParentProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    # permission_classes = [permissions.IsAuthenticated, ]
    serializer_class = ParentProductSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["category__name", "name", "description","staffRecommended","brand"]
'''
# class ProductViewSet(viewsets.ModelViewSet):
#     queryset = Product.objects.all()
#     permission_classes=(AllowAny,)
#     # permission_classes = [permissions.IsAuthenticated, ]
#     serializer_class = ProductSerializer
#     filter_backends = [SearchFilter, OrderingFilter]
#     search_fields = ["category__title", "name", "description"]
#     ordering_fields = ("category__title", "name", "product_size_color__price")

#     def create(self,request):
#         serializer=ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             print('##############################################')
#             serializer.save()
#             print(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ProductSerializer
    template_name = "products/index.html"
    authentication_classes = (
        CsrfExemptSessionAuthentication, BasicAuthentication)

    @csrf_exempt
    def get(self, request):
        queryset = Product.objects.all()
        prod = []
        for product in queryset:
            psc = Product_Size_Color.objects.filter(product=product)
            
            obj = Product_Images.objects.filter(product_size_color=psc[0])[0]
            print(obj)
        
            prod.append((product, psc, obj))
        paginator = Paginator(prod, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return Response({'page_obj': page_obj})


class ProductDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    serializer_class = ProductSerializer
    template_name = "products/detail.html"
    # authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    # @csrf_exempt

    def get(self, request, pk):
        queryset = Product.objects.get(pk=pk)
        psc = Product_Size_Color.objects.filter(product=queryset)
        review = Reviews.objects.filter(product=pk)
        prod = []
        for p in psc:
            obj = Product_Images.objects.filter(product_size_color=p)
            prod.append((p, obj))
            if request.auth:
                wishlists = Wishlist.objects.filter(owner=request.user)
            else:
                wishlists = []
        return Response({'product': queryset, 'psc': prod, 'wishlists': wishlists, 'reviews': review})

# https://stackoverflow.com/questions/41094013/when-to-use-serializers-create-and-modelviewsets-create-perform-create
