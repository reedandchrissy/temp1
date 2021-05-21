import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class ProductFilter(django_filters.FilterSet):
    note = CharFilter(field_name='name', lookup_expr='icontains')
    class Meta:
        model = Product
        fields = ['category']


class OrderFilter(django_filters.FilterSet):


    class Meta:
        model = OrderItem
        fields = '__all__'
        exclude = ['date_added', 'quantity']

class OrderMatchFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='date_ordered', lookup_expr='gte')
    end_date = DateFilter(field_name='date_ordered', lookup_expr='lte')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['date_ordered']



class DeliveryFilter(django_filters.FilterSet):
    class Meta:
        model = ShippingAddress
        fields = ['order', 'customer']
