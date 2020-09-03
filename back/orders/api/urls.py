from django.urls import path, include
from orders.api.views import *
from rest_framework import routers

# router = routers.SimpleRouter()
#router.register("orders", OrderViewSet,basename="order")

urlpatterns = [
    path("orders/", OrderList.as_view(), name='orderlist'),
    path("orders/<int:pk>", OrderDetail.as_view(), name='orderdetail'),
    path("orders/checkout/", OrderCreate.as_view(), name="order-checkout"),
    path('orders/next/', nextfn, name='next'),
]
