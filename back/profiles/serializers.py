from rest_framework import serializers
from .models import Customer_Profile, Address, Card_Detail
from accounts.serializers import UserSerializer


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class CardDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card_Detail
        fields = '__all__'


class CustomerProfileSerializer(serializers.ModelSerializer):
    # customer=UserSerializer()
    # address=AddressSerializer(many=True)
    # cards=CardDetailSerializer(many=True)
    phone_number = serializers.CharField(max_length=10)

    def validate_phone_number(self, data):
        print('sssssssssssssssssssssssssssssssssssssssssssssssss')
        if not (data.isdigit() and len(data) == 10):
            raise ValidationError(
                '%(phone)s must be 10 digits', params={'phone': data},)
        return data

    class Meta:
        model = Customer_Profile
        fields = ('firstname', 'lastname', 'phone_number',)
        extra_kwargs = {'phone_number': {'validators': []}}
