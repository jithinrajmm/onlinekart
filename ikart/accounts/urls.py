from django.urls import path,include
from . import views

urlpatterns = [
    path('register/',views.register,name="register"),
    path('register/<str:recomended_code>/',views.register,name="register"),
    path('login/',views.login,name="login"),

    path('signout_user/',views.signout_user,name="signout_user"),

    path('otp_generate',views.otp_generate,name='otp_generate'),
    path('otp_checking',views.otp_checking,name='otp_checking'),
    

    path('user_profile',views.user_profile,name='user_profile'),
    path('user_images',views.user_images,name='user_images'),
    
    
    path('collect_address/',views.collect_address,name='collect_address'),
    path('view_address/',views.view_address,name='view_address'),
    path('collect_address_user/',views.collect_address_user,name='collect_address_user'),
    path('save_address/',views.save_address,name='save_address'), 
    path('delete_address/<int:address_id>/',views.delete_address,name='delete_address'),
    path('edit_address/<int:address_id>/',views.edit_address,name='edit_address'),

    path('forgott_password/',views.forgott_password,name='forgott_password'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),
    
    
    
]