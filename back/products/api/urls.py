# from django.urls import path, include
# from rest_framework.routers import SimpleRouter
# from products.api.views import ProductViewSet,CategoryViewSet

# router = SimpleRouter()
# router.register("categories",CategoryViewSet)
# router.register("products", ProductViewSet)

# urlpatterns = [path("", include(router.urls)),
# ]
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from products.api.views import ProductList, CategoryViewSet, ProductDetail
from products.views import *
router = SimpleRouter()
router.register("categories", CategoryViewSet)
# router.register("products", ProductViewSet)

urlpatterns = [
    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path('searchhome/', searchhome, name='search-home'),

]
