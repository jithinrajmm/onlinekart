from django.core.exceptions import ObjectDoesNotExist
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from accounts.models import Account,UserAddress
from cart.models import Cart,CartItem
from django.contrib.auth.decorators import login_required


#getting the session id for checking the cart id is equal to session id

def _cart_id(request):
    

    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
 
def add_cart(request, product_id):

    print('this is in cart aadiing views')
    current_user = request.user
    product = Product.objects.get(id = product_id)

    if current_user.is_authenticated:

        is_cart_item_exists = CartItem.objects.filter(product = product, user = current_user).exists()
        if is_cart_item_exists:
            cart_item= CartItem.objects.filter(product= product, user= current_user)
        try:
            cart_item= CartItem.objects.get(product= product, user= current_user)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                user = current_user ,
            )
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        
        try:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            print(_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id= _cart_id(request))
        cart.save()
        try:
            cart_item= CartItem.objects.get(product= product, cart= cart)
            cart_item.quantity += 1
            cart_item.save()

        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(
                product = product,
                quantity = 1,
                cart = cart
            )
            cart_item.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return redirect('cart')
    # print(product_id)

    # # current_user = request.user
    # product = Product.objects.get(id = product_id) # get the product
    # print(product)

    # if request.user.is_authenticated:
    #     print("dddddddddddddddddddddddddddddd",request.user)

    #     try:
    #         cart= Cart.objects.get(cart_id=_cart_id(request)) # get the product based on the session id that present in category table
    #     except Cart.DoesNotExist:
    #         cart= Cart.objects.create(cart_id=_cart_id(request)) 

    #     cart.save()
    #     try:
    #         cart_items= CartItem.objects.get(product=product,cart=cart)
    #         cart_items.quantity+=1
    #         cart_items.save()
    #     except CartItem.DoesNotExist:
    #         cart_items=CartItem.objects.create(
    #             product=product,
    #             cart=cart,
    #             quantity=1,
    #             user=request.user
                
    #         )
    #         cart_items.save()

    # else:

    #     try:
    #         cart= Cart.objects.get(cart_id=_cart_id(request)) # get the product based on the session id that present in category table
    #     except Cart.DoesNotExist:
    #         cart= Cart.objects.create(cart_id=_cart_id(request)) 

    #     cart.save()
    #     try:
    #         cart_items= CartItem.objects.get(product=product,cart=cart)
    #         cart_items.quantity+=1
    #         cart_items.save()
    #     except CartItem.DoesNotExist:
    #         cart_items=CartItem.objects.create(
    #             product=product,
    #             cart=cart,
    #             quantity=1
                
    #         )
    #         cart_items.save()        
    # # return HttpResponse(cart_items.quantity)
    # return redirect('cart')


    
    
 

def cart(request,total=0,quantity=0,cart_items=None):

    grand_total=0
    try:
        if request.user.is_authenticated:
            # print(request.user)
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:    
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for kart_items in cart_items:
            # total= total+ (kart_items.product.price * kart_items.quantity)
            # quantity+= kart_items.quantity

            # this code after adding offer price
            if kart_items.product.product_offer_price:

                total=total+(kart_items.product.product_offer_price * kart_items.quantity)

            elif kart_items.product.category_offer_price:

                total=total+(kart_items.product.category_offer_price* kart_items.quantity)

            else:
                total= total+ (kart_items.product.price * kart_items.quantity)
            
            quantity+= kart_items.quantity

        grand_total= total
    except ObjectDoesNotExist:
        pass

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':grand_total
    }                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           
    return render(request,'ekarthomes/cart.html',context)



    # try:
    #     cart=Cart.objects.get(cart_id=_cart_id(request))
    #     if request.user.is_authenticated:
    #         cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        
    #     cart_items=CartItem.objects.filter(cart=cart,is_active=True)
    #     for kart_items in cart_items:
    #         total= total+ (kart_items.product.price * kart_items.quantity)
    #         quantity+= kart_items.quantity


    # except ObjectDoesNotExist:
    #     pass

    # context={
    #     'total':total,
    #     'quantity':quantity,
    #     'cart_items':cart_items,
    #     'grand_total':total,

    
    # }


    # return render(request,'ekarthomes/cart.html',context)

# it is used to decreasing the items from cart

def remove_cart(request,product_id):

    product=get_object_or_404(Product,id=product_id)

    try:
        if request.user.is_authenticated:

           cart_item = CartItem.objects.get(product = product,user = request.user)
        else:  
           cart=Cart.objects.get(cart_id =_cart_id(request)) 
           cart_item = CartItem.objects.get(product=product,cart=cart)

        if cart_item.quantity > 1:
           cart_item.quantity -= 1
           cart_item.save()
        else:
           cart_item.delete()
    except:
        pass       
    return redirect('cart') 

    # cart= Cart.objects.get(cart_id=_cart_id(request))
    # product=get_object_or_404(Product,id=product_id)
    # cart_item=CartItem.objects.get(product=product, cart=cart)
    # if cart_item.quantity>1:
    #     cart_item.quantity-=1
    #     cart_item.save()
    # else:
    #     cart_item.delete()
    # return redirect('cart')



def delete_cart_items(request,product_id):

    product=get_object_or_404(Product,id=product_id)

    

    if request.user.is_authenticated:
        cart_item=CartItem.objects.get(product=product,user=request.user)
    else:
        cart= Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()

    return redirect('cart')
    

# Create your views here.

# checkout function

@login_required(login_url='login')
def checkout(request,total=0,quantity=0,cart_items=None):

    try:
        # cart=Cart.objects.get(cart_id=_cart_id(request))
        # cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        if request.user.is_authenticated:
            cart_items=CartItem.objects.filter(user=request.user,is_active=True)
        else:    
            cart=Cart.objects.get(cart_id=_cart_id(request))
            cart_items=CartItem.objects.filter(cart=cart,is_active=True)
        for kart_items in cart_items:
            if kart_items.product.product_offer_price:
                total=total+(kart_items.product.product_offer_price * kart_items.quantity)
            elif kart_items.product.category_offer_price:
                total=total+(kart_items.product.category_offer_price* kart_items.quantity)
            else:
                total= total+ (kart_items.product.price * kart_items.quantity)
            quantity+= kart_items.quantity


            # this is the code before adding offers
            # total= total+ (kart_items.product.price * kart_items.quantity)
            # quantity+= kart_items.quantity

    except ObjectDoesNotExist:
        pass
    addresses=UserAddress.objects.filter(user=request.user)

    context={
        'total':total,
        'quantity':quantity,
        'cart_items':cart_items,
        'grand_total':total,
        'addresses':addresses

    
    }
    # return render(request,'ekarthomes/checkout.html',context)
    return render(request,'ekarthomes/place_orders.html',context)
    # return HttpResponse('helllllllllo checkout')
