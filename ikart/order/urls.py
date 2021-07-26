from django.urls import path,include
from . import views

urlpatterns = [
    path('place_order/', views.place_order, name="place_order"),
    path('payment/<int:order_id>/', views.payment, name="payment"),
    path('view_orders',views.view_orders,name='view_orders'),

    path('product_track/<int:orderd_product_id>/',views.product_track,name='product_track'),
    path('cancel_order/<int:product_id>/',views.cancel_order,name='cancel_order'),


    path('paypal_payment/',views.paypal_payment,name='paypal_payment'),
    path('razor_pay',views.razor_pay,name='razor_pay'),
    path('order_complete/',views.order_complete,name='order_complete'),
    path('invoice/',views.invoice,name='invoice'),

    path('coupon_checking_ajax/',views.coupon_checking_ajax,name='coupon_checking_ajax'),

    
    
    

   



    
    
    # path('remove_cart/<int:product_id>/', views.remove_cart, name="remove_cart"),

] 