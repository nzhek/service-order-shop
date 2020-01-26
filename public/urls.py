from django.urls import path
from public.views import index, orders, sign_out
from django.contrib.auth import views

urlpatterns = [
    path('', index, name='index-page'),
    path('orders/', orders, name='orders-page'),
    path('sign-out/', views.LogoutView.as_view(), name='sign_out'),
]
