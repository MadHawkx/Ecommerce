from django.shortcuts import render
from .models import Product_Size_Color, Product, Size, Color, Category
from django.db import connection
from .filters import ProductFilterHome, ProductFilter
from django.core.paginator import Paginator

# Create your views here.


# def view_products(request):
#     products = Product_Size_Color.objects.prefetch_related(
#         'product__category').all()
#     abc = []
#     for pr in products:
#         cat = pr.product.category.all()
#         abc.append((pr, cat))
#     paginator = Paginator(abc, 1)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "prod.html", {'products': abc})


def searchhome(request):
    product_list = Product.objects.all()
    query = request.GET.get('q', False)
    if query:
        request.session['query'] = query
    product_filter = ProductFilterHome(request.GET, queryset=product_list)
   # product_filter = ProductFilterHome(query, queryset=product_list)
    filter_on = ProductFilter(request.GET, queryset=product_filter.qs)

    paginator = Paginator(filter_on.qs, 5)
    page = request.GET.get('page')
    response = paginator.get_page(page)
    return render(request, 'products/search.html', {'sizes': Size.objects.values('size'), 'colors': Color.objects.values('color'), 'cats': Category.objects.values('title'), 'brands': product_list.values('brand'), 'filter': response, 'filterform': product_filter, 'filter2': filter_on, 'q': query})
