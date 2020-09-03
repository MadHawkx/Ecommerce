from django.urls import path, include, re_path
from .views import *
urlpatterns = [
    path('', CustomerProfileDetail.as_view(), name="profile_detail"),
    path('update/', CustomerProfileUpdate.as_view(), name="profile-update"),

    path('addresses/<int:pk>', CustomerAddressDetail.as_view(), name="addressedit"),
    path('addresses/<int:pk>/delete/', CustomerAddressDelete.as_view()),
    path('addresses/create/', CustomerAddressCreate.as_view()),
    path('addresses/', CustomerAddressList.as_view(), name='addresslist'),

    path('cards/<int:pk>', CustomerCardDetail.as_view(), name="cardedit"),
    path('cards/<int:pk>/delete/', CustomerCardDelete.as_view()),
    path('cards/create/', CustomerCardCreate.as_view()),
    path('cards/', CustomerCardList.as_view(), name="cardlist"),
    path('validate_phone', PhoneVerification.as_view(), name='phone-verify'),

]
