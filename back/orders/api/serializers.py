from rest_framework import serializers
from orders.models import Order, OrderItem
from profiles.models import Address
from cart.models import Cart, CartItem
from profiles.serializers import AddressSerializer
from cart.api.serializers import UserSerializer
from products.api.serializers import ProductSizeColorSerializer
# from .tasks import order_created


class OrderItemSerializer(serializers.ModelSerializer):
    item = ProductSizeColorSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ('id', 'ordered', 'item', 'quantity', 'received',
                  'replacement_requested', 'replaced', 'refund_requested', 'refunded')


class OrderSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserSerializer(read_only=True)
    orderitems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'address',
                  'ordered_date', 'ordered', 'orderitems')
        read_only_fields = ['ordered', 'id', 'ordered_date', ]

    def create(self, validated_data):
        if(self.context['address_id']):
            address = validated_data.pop('address')
            order = Order(**validated_data)
            order.user = self.context['request'].user
            order.address = Address.objects.get(id=self.context['address_id'])
            order.save()
        else:
            address = validated_data.pop('address')
            ad = Address.objects.create(**address)
            order = Order(**validated_data)
            order.user = self.context['request'].user
            order.address = ad
            order.save()
        # order_created(order.id)
        # self.context['request'].session['order_id'] = order.id
        for cartitem in self.context['cartitems']:
            if cartitem.quantity < cartitem.item.quantity:
                OrderItem.objects.create(
                    order=order, item=cartitem.item, quantity=cartitem.quantity)
            else:
                raise serializers.ValidationError({'status': 'quantity error'})
        order.total = order.get_total_cost()
        order.save()
        return order
