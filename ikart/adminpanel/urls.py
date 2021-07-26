from django.urls import path
from . import views

urlpatterns = [
    path('add_product',views.add_product,name='add_product'),
    path('',views.loginadmin,name="loginadmin"),
    path('userview',views.userview,name='userview'),
    path('adminhome',views.adminhome,name='adminhome'),
    path('category',views.category,name='category'),
    path('viewcategory',views.viewcategory,name='viewcategory'),
    path('edit_category/<int:id>', views.edit_category, name='edit_category'),
    path('delete_category/<int:id>', views.delete_category, name='delete_category'),
    path('activeuser/<int:id>', views.delete_category, name='delete_category'),

    path('view_product',views.view_product,name='view_product'),
    path('delete_product/<int:id>',views.delete_product,name='delete_product'),
    path('activeUser/<int:id>',views.activeUser,name='activeUser'),
    path('adminFlush',views.adminFlush,name='adminFlush'),
    path('edit_product/<int:id>',views.edit_product,name='edit_product'),
    
    path('delete_product',views.delete_product,name='delete_product'),
    path('order_details/',views.order_details,name='order_details'),
    path('order_status/<int:id>/',views.order__product_status,name='order_status'),

    path('report_genaration',views.report_genaration,name='report_genaration'),
    path('month_report',views.month_report,name='month_report'), 
    path('yearly_report',views.yearly_report,name='yearly_report'),
    path('date_report',views.date_report,name='date_report'),
    

    path('coupon_adding/',views.coupon_adding,name='coupon_adding'),
    path('coupon_view/',views.coupon_view,name='coupon_view'),
    path('coupon_delete/<int:id>/',views.coupon_delete,name='coupon_delete'),
    path('add_refferal_coupon/',views.add_refferal_coupon,name='add_refferal_coupon'),
    
    

]