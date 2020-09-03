from cart.models import Cart, CartItem
from accounts.models import User
from rest_framework import serializers, viewsets
from django.db.models import FloatField
from products.api.serializers import ProductSerializer, ProductSizeColorSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email',)


class CartItemSerializer(serializers.ModelSerializer):
    item = ProductSizeColorSerializer()

    class Meta:
        model = CartItem
        fields = ('id', 'item', 'quantity')


class CartSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    cartitem = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ('id', 'customer', 'created_at', 'updated_at',
                  'cartitem', 'number_of_items', 'total')
    # def create(self,validated_data):
    #     customers=validated_data.pop('customer')
    #     cartitems=validated_data.pop('cartitem')
    #     cart


# https://github.com/jessanettica/simple-shopping-api/tree/master/ecommercesite

# https://www.django-rest-framework.org/api-guide/relations/#stringrelatedfield
# https://stackoverflow.com/questions/3090302/how-do-i-get-the-object-if-it-exists-or-none-if-it-does-not-exist
#go = SomeModel.objects.get(foo='bar')
# https://stackoverflow.com/questions/40540433/whats-the-difference-between-post-create-and-perform-create-in-views
# https://stackoverflow.com/questions/42615984/whats-the-difference-between-a-viewsets-create-and-update-and-a-seriali
# https://github.com/etherai/cart-api/tree/master/server/api/cart_api
