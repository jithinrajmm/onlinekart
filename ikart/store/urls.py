from django.urls import path,include
from . import views


urlpatterns = [
   
    # path('comp_details/<str:slug>',views.comp_details,name="comp_details"),
    path('', views.store_view, name="store"),
    path('category/<slug:category_slug>/<slug:product_slug>', views.product_details , name="product_details"),
    path('category/<slug:category_slug>/', views.store_view, name="product_by_category"),
    path('add_offer', views.add_offer, name="add_offer"),
    path('add_category_offer', views.add_category_offer, name="add_category_offer"),
    path('add_product_offer', views.add_product_offer, name="add_product_offer"),

    path('offer_view', views.offer_view, name="offer_view"),

    path('delete_cat_offer/<int:id>/', views.delete_cat_offer, name="delete_cat_offer"),

    path('delete_pro_offer/<int:id>/', views.delete_pro_offer, name="delete_pro_offer"),

    path('product_review/<int:product_id>/',views.product_review,name="product_review"),

    path('search/',views.search,name='search')


    

    

    
] 