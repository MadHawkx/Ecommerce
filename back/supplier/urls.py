from django.urls import path, re_path
from supplier.views import *
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('add_product', add_product, name="add_product"),
    path('display_product', display_product, name="display_product"),
    path('add_product_specifications/<product_id>',
         add_product_specifications, name="add_product_specifications"),
    path('register_supplier', register_supplier, name="register_supplier"),
    path('login_supplier', login_supplier, name="login_supplier"),
    path('logout_supplier', logout_supplier, name="logout_supplier"),
    path('password_reset', password_reset, name="password_reset"),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('activate_supplier/<slug:uidb64>/<slug:token>/',
         activate_supplier, name='activate_supplier'),
        path('update_password', update_password, name="update_password"),
    path('edit_product/<product_id>', edit_product, name="edit_product"),
    path('view_history/<product_id>', view_history, name="view_history"),
    path('delete_product/<product_id>', delete_product, name="delete_product"),
    path('ordered_products', ordered_products),
    path('validate_phone', validate_phone, name='validate_phone'),
    # path('supplier_profile', supplier_profile, name="supplier_password"),

]
