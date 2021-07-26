from category.models import Category
from django.shortcuts import render,get_object_or_404
from store.models import *



# Create your views here.
def index(request):

    offer_pro=ProductOffer.objects.all()
    
    today = date.today()
    today1 = today.strftime("%Y-%m-%d")
    for offer in offer_pro:
        print(offer.offer_end)
        if str(offer.offer_end) <= today1 :
            pro=Product.objects.get(id=offer.product.id)
            pro.product_offer_price=None
            pro.save(update_fields=['product_offer_price'])
             
        else:
            pass 
        
        
    Category_Offer=CategoryOffer.objects.all()
    
    today = date.today()
    today1 = today.strftime("%Y-%m-%d")
    print(today1)
    for offer in Category_Offer:
        print(offer.offer_end)
        if str(offer.offer_end) <= today1 :
            pro=Product.objects.filter(category=offer.category.id)
            for cat_ofr in pro:
                print(cat_ofr.category_offer_price)
                cat_ofr.category_offer_price=None
                cat_ofr.save(update_fields=['category_offer_price'])
             
        else:
            pass  

    product=Product.objects.all().filter(is_available=True)
    context={ 'products': product,
    'offer_pro': offer_pro,
    'Category_Offer':Category_Offer,
    
    
    }
    # return render(request,'storehtml/store/productview.html',context)
    
    return render(request,'ekarthomes/index.html',context)
    # return render(request,'accounts/reset_password.html')
    # D:\spsdjango\onlinekart\ikart\templates\adminpanel\baseadmin.html
    



