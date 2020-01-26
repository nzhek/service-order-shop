from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from api_v0.views import OrderView, OrderDateRange, CustomerView, orders_by_week

urlpatterns = format_suffix_patterns([
    path('orders/', OrderView.as_view(), name='orders'),
    path('orders/<int:pk>/', OrderView.as_view(), name='delete_orders'),
    path('orders-range/', OrderDateRange.as_view({'get': 'list'}), name='orders_date_range'),
    path('orders-by-week/', orders_by_week, name='orders_by_week'),
    path('customers/', CustomerView.as_view(), name='customers')
], allowed=['json'])

