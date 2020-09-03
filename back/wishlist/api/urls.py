from django.urls import path, include
from rest_framework.routers import DefaultRouter
from wishlist.api.views import *
from rest_framework import routers

urlpatterns = [
    path('wishlists/', WishlistList.as_view(), name='wishlistlist'),
    path('wishlists/<int:pk>/delete/',
         WishlistDelete.as_view(), name='wishlistdelete'),
    path('wishlists/<int:pk>/', WishlistDetail.as_view(), name='wishlistdetail'),
    path('wishlists/<int:pk>/rename/',
         WishlistEdit.as_view(), name='wishlistedit'),
    path('wishlists/create/', WishlistCreate.as_view(), name='wishlistcreate'),
    path('wishlists/<int:pk>/add_to_wishlist/',
         add_to_wishlist, name='addtowishlist'),
    path('wishlists/<int:pk>/remove_from_wishlist/',
         remove_from_wishlist, name='removefromwishlist'),

]
