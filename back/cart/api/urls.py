from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cart.api.views import CartDetail, CartList, add_to_cart, remove_from_cart, update_cart
from rest_framework import routers

urlpatterns = [
    path('cart/', CartDetail.as_view(), name='cart'),
    path('cart/add_to_cart/', add_to_cart),
    path('cart/remove_from_cart/', remove_from_cart),
    path('cart/update_cart/', update_cart),
]
