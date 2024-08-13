from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product_list', views.product_list, name='product_list'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('register/', views.register, name='register'),
    path('login/',views.login, name='login'),
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('logout/', views.logout, name='logout'),
    path('contact/', views.contact, name='contact'),
    path('order_confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]

