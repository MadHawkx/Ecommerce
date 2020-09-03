'''
from django.shortcuts import render

# Create your views here.
from rest_auth.registration.views import RegisterView
#from .serializers import  CustomRegisterSerializer
from .models import User

class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
    serializer_class =  CustomRegisterSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        custom_data = {"message": "some message", "status": "ok"}
        response.data.update(custom_data)
        return response

'''