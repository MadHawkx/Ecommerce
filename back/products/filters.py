import django_filters
from .models import Product, Product_Size_Color
from django.db.models import Q


class ProductFilterHome(django_filters.FilterSet):
    # title = django_filters.CharFilter(field_name='name', lookup_expr='exact', distinct=True)
    # category = django_filters.CharFilter(field_name='category__title', lookup_expr='exact', distinct=True)
    q = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Product
        # fields = [
        # 	'category',
        # 	'title',
        # ]
        fields = ['q']

    def __init__(self, *args, **kwargs):
        super(ProductFilterHome, self).__init__(*args, **kwargs)
        self.filters['q'].label = ''

    def my_custom_filter(self, queryset, name, value):
        return Product.objects.filter(Q(name__icontains=value) | Q(brand__icontains=value) | Q(category__title__icontains=value))


class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='category__title', lookup_expr='icontains', distinct=True)
    brand = django_filters.CharFilter(
        field_name='brand', lookup_expr='icontains', distinct=True)
    size = django_filters.CharFilter(
        field_name='product_size_color__size__size', lookup_expr='icontains', distinct=True)
    color = django_filters.CharFilter(
        field_name='product_size_color__color__color', lookup_expr='icontains', distinct=True)
    #category_id = django_filters.CharFilter(field_name='categories__id', lookup_expr='icontains', distinct=True)
    min_price = django_filters.CharFilter(
        field_name='product_size_color__price', lookup_expr='gte', distinct=True)  # (some_price__gte=somequery)
    max_price = django_filters.NumberFilter(
        field_name='product_size_color__price', lookup_expr='lte', distinct=True)
    #q = django_filters.CharFilter(method='my_custom_filter')

    class Meta:
        model = Product
        fields = [
            'min_price',
            'max_price',
            'size',
            'color',
        ]
        # fields = ['q']

    def __init__(self, *args, **kwargs):
        super(ProductFilter, self).__init__(*args, **kwargs)
        self.filters['min_price'].label = 'Min Price'
        self.filters['max_price'].label = 'Max Price'
        self.filters['size'].label = 'Sizes'
        self.filters['color'].label = 'Colors'
        self.filters['category'].label = 'Category'
        self.filters['brand'].label = 'Brand'
