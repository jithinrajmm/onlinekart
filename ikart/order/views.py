from json.encoder import py_encode_basestring
from django.core.checks import messages
from django.http.response import HttpResponse,JsonResponse
from django.shortcuts import render,redirect
from order.models import *
from cart.models import *
import datetime
import json
from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt


# Create your views here.


def place_order(request,total=0,quantity=0):
    coupon= request.session.get('coupon')
    print(coupon,'......................................................')

    # if kart_items=CartItem.objects.filter(user=request.user).exists():
    #     ret
    current_user=request.user

    cart_items=CartItem.objects.filter(user=request.user)
    cart_count=cart_items.count()

    print('count of cart itemsssssss',cart_count)

    if cart_count < 0 :
        return redirect('index1')

    sub_total=0
    deli_charge=100
    grand_total=0



    for kart_items in cart_items:
        # this is old before adding offers
        
        # total= total+ (kart_items.product.price * kart_items.quantity)

        # quantity+= kart_items.quantity
        # after adding offer
        # its onlly for displaying dataaaaaaaaaaaa

        if kart_items.product.product_offer_price:

            total=total+(kart_items.product.product_offer_price * kart_items.quantity)

        elif kart_items.product.category_offer_price:

            total=total+(kart_items.product.category_offer_price* kart_items.quantity)

        else:
            
            total= total+ (kart_items.product.price * kart_items.quantity)
            

    sub_total= total
    # if request.session.get('coupon_grand_total'):
    #     grand_total=float(request.session.get('grand_total',1))
    #     del request.session['coupon_grand_total']
    # else:
    if request.session.get('coupon'):
        print('hellooooo')
        coupon= request.session.get('coupon')
        if UsedOffer.objects.filter(user=request.user,coupen__coupon_code=coupon,is_orderd=False).exists():
            print('in thjisss djfkjsjghkjsfn')
            
            usedoffer=UsedOffer.objects.get(user=request.user, coupen__coupon_code=coupon, is_orderd=False)
            print(usedoffer,'this is used offer')
            percentge=usedoffer.coupen.coupon_percentage
            grand_total=sub_total-sub_total*percentge/100
        elif RefferalCoupen.objects.filter(user=request.user,ref_coupon=coupon).exists():
            referal_offer=RefferalCoupen.objects.get(user=request.user,ref_coupon=coupon)
            percentge=referal_offer.ref_percentage
            grand_total=sub_total-sub_total*percentge/100
        else:
            pass
            
    else:
        grand_total=sub_total
    
    # request.session['coupon_percentege'] = coupen.coupon_percenta
    if request.method == 'POST':

        addres_permission=request.POST.get('address',False)
    
        if addres_permission=='address':
            data=request.POST

            user_address= UserAddress()
            

            if UserAddress.objects.filter(first_name=data['first_name'],last_name=data['last_name'],phone=data['phone'],email=data['email'],address_line1=data['address_line_1'],address_line2=data['address_line_2'],state=data['state'],city=data['city'],user=request.user.id).exists():
                messages.Info(request,'address already exist')
                print('exist')

            else:
                
                user_address.user=request.user
                user_address.first_name=data['first_name']
                user_address.last_name=data['last_name']
                user_address.phone=data['phone']
                user_address.email=data['email']
                user_address.address_line1=data['address_line_1']
                user_address.address_line2=data['address_line_2']
                user_address.state=data['state']
                user_address.city=data['city']
                user_address.save()
                
        data=request.POST

        if Order.objects.filter(user=request.user,is_ordered=False).exists():
            order= Order.objects.get(user=request.user,is_ordered=False)
        else:
            order=Order()

        

        order.first_name=data['first_name']
        order.last_name=data['last_name']
        order.phone=data['phone']
        order.email=data['email']
        order.address_line1=data['address_line_1']
        order.address_line2=data['address_line_2']
        order.state=data['state']
        order.city=data['city']
        order.order_note=data['order_note']
        order.order_total=grand_total
        order.deli_charge=deli_charge
        order.ip=request.META.get('REMOTE_ADDR')
        order.user=request.user
        # order.order=Order(first_name=first_name,last_name=last_name,phone=phone,email=email,address_line1=address_line1,address_line2=address_line2,state=state,city=city,order_note=order_note,ip=ip,tax=tax,order_total=order_total)
        order.save()
        request.session['order_id']=order.id

        """ this is used to genarate the order separated id with date and order id """

        yr=int(datetime.date.today().strftime('%Y'))
        dt=int(datetime.date.today().strftime('%d'))
        mt=int(datetime.date.today().strftime('%m'))
        d=datetime.date(yr,mt,dt)
        current_date=d.strftime("%Y%m%d")  #generate id with based on date
        order_number=current_date+str(order.id)
        
        order.order_number=order_number
        order.save()
        order_details=Order.objects.get(user=current_user,is_ordered=False,order_number=order_number)
        
        razer_pay_total=grand_total*100

        context={

            'order_user':order_details,
            'cart_items':cart_items,
            'grand_total':grand_total,
            'razer_pay_total':razer_pay_total,
            'sub_total':sub_total,
            'deli_charge':deli_charge,

        }
        request.session['order_number']=order_details.order_number
        return render(request,'ekarthomes/payment_methode.html',context)
    return redirect('index1')

# cod
def payment(request,order_id):  
 
    if request.method == 'POST':

        order_info=Order.objects.get(user=request.user,is_ordered=False,order_number=order_id)
        cart_items=CartItem.objects.filter(user=request.user)
        pay='cod'

        payment=Payment(user=request.user,amount_paid=order_info.order_total,payment_id=order_id,payment_method=pay,satus="pending")
        payment.save()
        order_info.payment=payment
        order_info.is_ordered=True
        order_info.save()

        for item in cart_items:

            orderproduct=OrderProduct()
            orderproduct.order=order_info
            orderproduct.user=request.user
            orderproduct.payment=payment
            orderproduct.product=item.product
            orderproduct.quantity=item.quantity
            #          if item.product.product_offer_price:

            #     total=total+(item.product.product_offer_price * item.quantity)

            # elif item.product.category_offer_price:

            #     total=total+(item.product.category_offer_price* item.quantity)

            # else:
                
            #     total= total+ (item.product.price * item.quantity)
            if item.product.product_offer_price:

                orderproduct.product_price=item.product.product_offer_price

            elif item.product.category_offer_price:

                orderproduct.product_price=item.product.category_offer_price
            else:

                orderproduct.product_price=item.product.price

            
            orderproduct.ordered=True
            orderproduct.save()

            product=Product.objects.get(id=item.product_id)
                
            print(product)

            product.stock -= item.quantity
            product.save()
        if request.session.get('coupon'):
            coupon= request.session.get('coupon')

            if UsedOffer.objects.filter(user=request.user,coupen__coupon_code=coupon).exists():
                used_offer=UsedOffer.objects.get(user=request.user,coupen__coupon_code=coupon)
                used_offer.is_orderd=True
                used_offer.save()

            elif RefferalCoupen.objects.filter(user=request.user,ref_coupon=coupon):
                referal_coupon=RefferalCoupen.objects.filter(user=request.user,ref_coupon=coupon)
                referal_coupon.delete()


        cart_items.delete()

    return render(request,'ekarthomes\success.html')


def view_orders(request):


    product_view=OrderProduct.objects.filter(user=request.user)
    

    context={

        'order_product': product_view,
        
    
    }
        
    
    return render(request,'ekarthomes/pdoduct_list.html',context)

# 

def product_track(request,orderd_product_id):

    single_product=OrderProduct.objects.get(id=orderd_product_id)
    # print('seeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee',single_product)
    context={
        'single_product':single_product,
    }
    return render(request,'ekarthomes/ordder_status.html',context)


# cancelling order

def cancel_order(request,product_id):

    ordered_product=OrderProduct.objects.get(id=product_id)
    ordered_product.user_cancelled=True
    ordered_product.status='Cancelled'
    ordered_product.product.stock+=ordered_product.quantity
    ordered_product.save()
    ordered_product.product.save()

    return redirect('product_track',product_id)


# paypal view
# store transaction details in this view

def paypal_payment(request):

    body=json.loads(request.body)
    order=Order.objects.get(user=request.user,is_ordered=False,order_number=body['orderID'])

    payment=Payment(user=request.user,payment_id=body['trans_ID'],
    payment_method=body['payment_method'],
    amount_paid=order.order_total,
    satus=body['status'])
    payment.save()
    order.payment=payment
    order.is_ordered=True
    order.save()
    cart_items=CartItem.objects.filter(user=request.user)
    for item in cart_items:

        # adding cartitems to product details table

        print('itenm saved')
        orderproduct=OrderProduct()
        orderproduct.order=order
        orderproduct.user=request.user
        orderproduct.payment=payment
        orderproduct.product=item.product
        orderproduct.quantity=item.quantity
        # orderproduct.product_price=item.product.price
        if item.product.product_offer_price:

            orderproduct.product_price=item.product.product_offer_price

        elif item.product.category_offer_price:

            orderproduct.product_price=item.product.category_offer_price
        else:

            orderproduct.product_price=item.product.price

        orderproduct.ordered=True
        orderproduct.save()
     # decreasing product quantity

        product=Product.objects.get(id=item.product_id)        
        print(product)
        product.stock -= item.quantity
        product.save()
    if request.session.get('coupon'):
            coupon= request.session.get('coupon')

            if UsedOffer.objects.filter(user=request.user,coupen__coupon_code=coupon).exists():
                used_offer=UsedOffer.objects.get(user=request.user,coupen__coupon_code=coupon)
                used_offer.is_orderd=True
                used_offer.save()

            elif RefferalCoupen.objects.filter(user=request.user,ref_coupon=coupon):
                referal_coupon=RefferalCoupen.objects.filter(user=request.user,ref_coupon=coupon)
                referal_coupon.delete()

    # clear cart
    cart_product=CartItem.objects.filter(user=request.user)
    cart_product.delete()

    # del request.session['coupon_grand_total']

    print(body)
    print("data recieved")

    data={
        'order_number':order.order_number,
        'transID':payment.payment_id
    }   

    return JsonResponse(data)


# Paypal payment complete method

def order_complete(request):

    # {'orderID': '20210709151', 'trans_ID': '3CS87553WN617873H', 'payment_method': 'PayPal', 'status': 'COMPLETED'}
    # this is from json respose 'data' dict 
    order_number=request.GET.get('order_number')
    trans_id=request.GET.get('payment_id')


    try:

        order=Order.objects.get(order_number=order_number,is_ordered=True)
        order_product=OrderProduct.objects.filter(order_id=order.id)
        payment=Payment.objects.get(payment_id=trans_id)
        context={

            'order':order,
            'order_product':order_product,
            'order_number':order.order_number,
            'payment':payment
            
        }
        return render(request,'ekarthomes/paymentComplete.html',context)
    except (Payment.DoesNotExist,Order.DoesNotExist):

        return redirect('index1')



        


def razor_pay(request):

    # return render(request,'ekarthomes/razer_payComplete.html'

    if request.method=='POST':

        global order_id

        order_id=request.POST.get('order_id')
        print(order_id)
        print(type(order_id))
        order=Order.objects.get(user=request.user,order_number=order_id,is_ordered=False)
        payment=Payment(user=request.user,payment_id=order_id,payment_method='razorpay',amount_paid=order.order_total,satus='completed')
        payment.save()
        order.payment=payment
        order.is_ordered=True
        order.save()
        cart_items=CartItem.objects.filter(user=request.user)


        for items in cart_items:

            order_product = OrderProduct()
            order_product.order=order
            order_product.payment=payment
            order_product.user=request.user
            order_product.quantity=items.quantity
            order_product.product=items.product
            
            # order_product.product_price=items.product.price
            # if items.product.product_offer_price:

            #     order_product.product_price=items.product.product_offer_price

            # elif items.product.category_offer_price:

            #     order_product.product_price=items.product.category_offer_price

            # else:

            order_product.product_price=items.product.price

            # order_product.product=items.product
    
            order_product.ordered=True
            order_product.status='Accepted'
            order_product.save()


            product=Product.objects.get(id=items.product_id)
            product.stock -= product.stock-items.quantity
            product.save()

        if request.session.get('coupon'):
            coupon= request.session.get('coupon')

            if UsedOffer.objects.filter(user=request.user,coupen__coupon_code=coupon).exists():
                used_offer=UsedOffer.objects.get(user=request.user,coupen__coupon_code=coupon)
                used_offer.is_orderd=True
                used_offer.save()
                del request.session['coupon']

            elif RefferalCoupen.objects.filter(user=request.user,ref_coupon=coupon):
                referal_coupon=RefferalCoupen.objects.filter(user=request.user,ref_coupon=coupon)
                referal_coupon.delete()
                del request.session['coupon']
            

            print(product)
        cart_items=CartItem.objects.filter(user=request.user)
        cart_items.delete()
        
       
       

        order=Order.objects.get(order_number=order_id,is_ordered=True)
        # 20210709154
        print(order)
        order_product=OrderProduct.objects.filter(order_id=order.id)
        print("hiaiiiii",order_product)
        print("pay",payment)
        order_address=Order.objects.get(user=request.user,order_number=order_id)
        print("user",order_address)

        context={

                'order': order,
                'order_product': order_product,
                'order_number': order.order_number,
                'payment':payment,
                'address':order_address
            
            }
        return render(request,'ekarthomes/paymentComplete.html',context)
        # except (Payment.DoesNotExist,Order.DoesNotExist):
        #         return redirect('index1')

    


   # OPTIONALclient.order.create(amount=order_amount, currency=order_currency, receipt=order_receipt, notes=notes)
    

@csrf_exempt
def success(request):
    return render(request, "success.html")

def invoice(request):

    order_number=request.session.get('order_number')
    print('this is from the session',order_number)
      
    order=Order.objects.get(order_number=order_number)
    
    order_product=OrderProduct.objects.filter(order=order_number)

    
    context={
        'order': order,
        'order_product': order_product,
    }
    return render(request,'ekarthomes/paymentComplete.html',context)


def coupon_checking_ajax(request):

    if request.method=='GET':
        data=request.GET.get('data')
        
        total= float(request.GET.get('grand_total'))
     
        
        if Coupon_add.objects.filter(coupon_code=data).exists():
            coupen=Coupon_add.objects.get(coupon_code=data)
            end_date= coupen.expire_date()

            if end_date:

                if UsedOffer.objects.filter(user=request.user,coupen=coupen,is_orderd=True).exists():
                    return JsonResponse({'couponUsed':True,'message':"Coupon already used" })

                else:
                    if UsedOffer.objects.filter(user=request.user,coupen=coupen,is_orderd=False).exists():
                        usedoffer=UsedOffer.objects.get(user=request.user, coupen=coupen, is_orderd=False)

                    else:
                        usedoffer=UsedOffer()


                    request.session['coupon']=data

                    coupon=Coupon_add.objects.get(coupon_code=data)
                    percentage=coupon.coupon_percentage
                    grand_total=total- (total * percentage)/100
                    offerPrice=(total * percentage)/100

                    usedoffer.user=request.user
                    usedoffer.coupen=coupon
                    usedoffer.save()
            
                    return JsonResponse({'couponUsed':False,'message':"Coupon applied" ,'total':grand_total,'offerPrice':offerPrice})
            else:
                return JsonResponse({'couponUsed':True,'message':"Coupon expired" })


            
        elif RefferalCoupen.objects.filter(ref_coupon=data,user=request.user).exists():

            # order_id=request.session.get('order_id')
            # referal_coupon=RefferalCoupen.objects.get(user=request.user,ref_coupon=data)
            # order=Order.objects.get(id=order_id,user=request.user)

            # percentage=referal_coupon.ref_percentage
            # total=order.order_total
            # grand_total=total-(total*percentage/100)
            # offerPrice=total*percentage/100

            # request.session['coupon_grand_total'] = grand_total

            # order.order_total=grand_total
            # order.save()

            # referal_coupon.delete()


            request.session['coupon']=data
            print('sssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss',data)
            referal_coupon = RefferalCoupen.objects.get(user=request.user,ref_coupon=data)
            percentage = referal_coupon.ref_percentage
            grand_total= total-(total*percentage/100)
            offerPrice = total*percentage/100

            return JsonResponse({'couponUsed':False,'message':"Coupon applied" ,'total':grand_total,'offerPrice':offerPrice,'razorpay':grand_total*100})

            
        else:
            return JsonResponse({'couponUsed':True,'message':"Invalid Coupon"})

            

      


    