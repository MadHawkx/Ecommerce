from django.urls import path, include, re_path
#from .views import CustomRegisterView
#from rest_auth.registration.views import VerifyEmailView, RegisterView
from rest_framework.authtoken import views
urlpatterns = [
    path('', include('allauth.urls')),
    # path('',include('rest_auth.urls')),
    # path('register/',CustomRegisterView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api-token-auth/', views.obtain_auth_token),
]
