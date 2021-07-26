from django.contrib import messages
from django.http.response import HttpResponse
from category.models import Category
from django.shortcuts import redirect, render,get_object_or_404
from store.models import Product
from cart.models import Cart,CartItem
from cart.views import _cart_id
from .models import *
from .forms import *
from order.models import *

from django.db.models import Q

from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator


# search functionality for the website
def search(request):
    if 'keyword' in request.GET:
        keyword=request.GET['keyword']
        if keyword:
            products=Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            context={
                'product':products,

            }
        
        
    return render(request,'ekarthomes/store.html',context)
    # return HttpResponse('jesus')
    

def product_details(request,category_slug,product_slug):
    
    

    if request.user.is_authenticated:

        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(user=request.user,product=single_product).exists()
        print(in_cart)
    else:
        single_product=Product.objects.get(category__slug=category_slug,slug=product_slug)
        in_cart=CartItem.objects.filter(cart__cart_id=_cart_id(request),product=single_product).exists()
        print(in_cart)
    
    if request.user.is_authenticated:
        try:
            order_product=OrderProduct.objects.filter(user=request.user,product=single_product.id).exists()
        except OrderProduct.DoesNotExist:
            order_product=None
    else:
        order_product=None


    review=ReviewRating.objects.filter(product__id=single_product.id)

    context={
        'single_pruduct':single_product,
        'in_cart':in_cart,
        'order_product':order_product,
        'reviews':review,
    }
    return render(request,'ekarthomes/productdetail.html',context)


def store_view(request,category_slug=None):

    categories=None
    product=None
    if category_slug != None:
        categories= get_object_or_404(Category,slug=category_slug)
        storepage_product=Product.objects.filter(category=categories)
        paginator=Paginator(storepage_product,3)
        page=request.GET.get('page')
        paginated_pages=paginator.get_page(page)
        product_count=storepage_product.count()

    else:
        storepage_product = Product.objects.all().filter(is_available=True)
        paginator=Paginator(storepage_product,3)
        page=request.GET.get('page')
        paginated_pages=paginator.get_page(page)
        product_count=storepage_product.count()

    context= {
         'product':paginated_pages,
         'count':product_count,

    }
    return render(request,'ekarthomes/store.html',context)

def add_offer(request):

    category=Category.objects.all()
    products=Product.objects.all()
    context={

        'category':category,
        'products':products,
        }
    
    return render(request,'adminpanel/add_offer.html',context)


# Create your views here.
def add_category_offer(request):

    if request.method=='POST':
        category_id=int(request.POST['category'])

        start=request.POST['start']
        end=request.POST['end']
        percentage=int(request.POST['offer'])
        category=Category.objects.get(id=category_id)

        if CategoryOffer.objects.filter(category=category_id).exists():
            print('existing offer ')

            offer_category=CategoryOffer.objects.get(category=category_id)

        else:

            offer_category=CategoryOffer()

            print('not existing')
        

        offer_category.category=category
        offer_category.offer=percentage
        offer_category.offer_start=start
        offer_category.offer_end=end
        offer_category.save()

        print('savedddddd')
        

        category_products=Product.objects.filter(category=category_id)

        for product in category_products:
            product.category_offer_price=product.price - (product.price * percentage/100)
            product.save()


        return redirect('offer_view')

def add_product_offer(request):

    print('haiiiiiiii')

    if request.method=='POST':
        product_id=int(request.POST['product'])
        print(product_id)

        start=request.POST['start']
        print(start)
        end=request.POST['end']
        print(end)
        percentage=int(request.POST['offer'])
    
        single_product=Product.objects.get(id=product_id)
        if ProductOffer.objects.filter(product=product_id):
            print('product offer saved')
            product_offer=ProductOffer.objects.get(product=product_id)
        else:
            print('not existing the offer')
            product_offer=ProductOffer()

        product_offer.product = single_product
        product_offer.offer = percentage
        product_offer.offer_start = start
        product_offer.offer_end = end
        product_offer.save()
        single_product.product_offer_price=single_product.price-(single_product.price)*percentage/100
        single_product.save()

        return redirect('offer_view')

def offer_view(request):

    Category_offer=CategoryOffer.objects.all()
    product_offer=ProductOffer.objects.all()
    context={
        'Category_offer':Category_offer,
        'product_offer':product_offer
    }
    return render(request,'adminpanel/offer_view.html',context)
    
def delete_cat_offer(request,id):

    offer=CategoryOffer.objects.get(id=id)
    print(offer)
    pro=Product.objects.filter(category=offer.category)
    for pro in pro:
        pro.category_offer_price=None
        pro.save(update_fields=['category_offer_price'])

    offer.delete()    
        
    return redirect('offer_view')



def delete_pro_offer(request,id):

    offer=ProductOffer.objects.get(id=id)
    print(offer)
    pro=Product.objects.get(product_name=offer.product)
    print(pro)
    pro.product_offer_price=None
    pro.save()
    offer.delete()  
    return redirect('offer_view') 

def product_review(request,product_id):


    print("enterd to the dksajflkjsdkajfjj")
    # url=request.META.get('HTTP_reffer')
    url=request.META.get('HTTP_REFERER')
    if request.method=='POST':
        print("enterd to the dksajflkjsdkajfjj")
        try:
            print('review already exist')
            review=ReviewRating.objects.get(user__id=request.user.id,product__id=product_id)
            form=ReviewForm(request.POST,instance=review)
            form.save()
            messages.success(request, 'Thank you! Your review has been updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form=ReviewForm(request.POST)
            data=ReviewRating()
            if form.is_valid():

                print('in the forms')
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been submitted.')
                return redirect(url)
        


        







