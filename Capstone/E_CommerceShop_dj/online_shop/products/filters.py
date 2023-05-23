import django_filters
from django_filters import CharFilter, NumberFilter
from products.models import Product

class ProductsFilter(django_filters.FilterSet):
    price = django_filters.NumberFilter()
    price__gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
    price__lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    
    name = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['name', 'price']
        