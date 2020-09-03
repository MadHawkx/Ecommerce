from django.urls import path
from payments import views

urlpatterns = [
    path('', views.payment, name="payment"),
    path('success/', views.success, name="payment_success"),
    path('failure/', views.failure, name="payment_failure"),
    path('place_order/', views.back, name='success-redirect')
]
