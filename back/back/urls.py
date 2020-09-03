"""back URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url, include
from django.shortcuts import render
# from django_email_verification import urls as mail_urls
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('home.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('profiles/', include('profiles.urls')),
    path('api/', include('products.api.urls')),
    path('api/', include('cart.api.urls')),
    path('api/', include('wishlist.api.urls')),
    path('supplier/', include('supplier.urls')),
    path('payment/', include('payments.urls')),
    path('api/', include('orders.api.urls')),
    path('api/', include('reviews.api.urls')),
    #url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings'))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
