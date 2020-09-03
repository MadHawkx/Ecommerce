from rest_framework import serializers
from wishlist.models import Wishlist
from products.api.serializers import ProductSerializer
from accounts.models import User
from cart.api.serializers import UserSerializer


class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'owner', 'products', 'name')
