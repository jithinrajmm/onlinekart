from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.cart, name="cart"),
    path('remove_cart/<int:product_id>/', views.remove_cart, name="remove_cart"),
    path('delete_cart_items/<int:product_id>/', views.delete_cart_items, name="delete_cart_items"),
    path('add_cart/<int:product_id>/', views.add_cart, name="add_cart"),
    path('checkout/', views.checkout, name="checkout"),


] 