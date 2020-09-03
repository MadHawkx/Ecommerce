#from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
'''
class CustomRegisterSerializer(RegisterSerializer):

    email = serializers.EmailField(required=True)
    password1 = serializers.CharField(write_only=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', ''),
        }
'''


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)
        read_only_fields = ('email',)
