from rest_framework import serializers
from .models import Supplier_Account


class SupplierProfileSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(max_length=10)

    def validate_phone_number(self, data):
        print('sssssssssssssssssssssssssssssssssssssssssssssssss')
        if not (data.isdigit() and len(data) == 10):
            raise ValidationError(
                '%(phone)s must be 10 digits', params={'phone': data},)
        return data

    class Meta:
        model = Supplier_Account
        fields = ('name', 'phone_number',)
        extra_kwargs = {'phone_number': {'validators': []}}
