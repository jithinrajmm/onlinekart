from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from accounts.models import Account
from category.models import Category
from . forms import *
from order.forms import *
from django.contrib import messages
from store.models import Product
from django.contrib.sessions.models import Session
from django.views.decorators.cache import never_cache
import base64
from django.core.files.base import ContentFile
from order.models import *
from django.db.models import Sum
from order.models import*
from store.models import *
from django.core.paginator import EmptyPage,PageNotAnInteger, Paginator

name='j'
password1=12345

@never_cache
def loginadmin(request):
    if request.session.get('logedin'):
        return redirect('adminhome')
    else:
        if request.method=="POST":
            adminname=request.POST['adminname']
            password=request.POST['password']

            if adminname==name and password1==int(password):
                request.session['logedin']=True
                return redirect('adminhome')
            elif adminname!=name or password!=password1:
                messages.info(request,'credential not correct')
                return redirect('loginadmin')
            # / home / jithin / PycharmProjects / ogpro2

        return render(request,'adminpanel/login.html')

@never_cache
def adminhome(request):

    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        # order=Order.objects.all()
        # product=Product.objects.all()
        # order_product=OrderProduct.objects.all()
        # product=Product.objects.filter(field_name__isnull=True).aggregate(Sum('field_name'))
        amount_cod= Payment.objects.filter(amount_paid=None).aggregate(Sum('amount_paid'))
        print(amount_cod)
        razorPay_Paypal = Payment.objects.filter(payment_method='razorpay') | Payment.objects.filter(payment_method='PayPal')
        sum_of_razor_paypayPal=0
        for amount in razorPay_Paypal:
            sum_of_razor_paypayPal+=amount.amount_paid

        razor_pay= Payment.objects.filter(payment_method='razorpay')

        razor_pay_amount=0

        for razor_pay in razor_pay:
            razor_pay_amount+= razor_pay.amount_paid

        pay_pal = Payment.objects.filter(payment_method='PayPal')
        pay_pal_amount=0

        for paypal in pay_pal:
            pay_pal_amount+=paypal.amount_paid

        cod = Payment.objects.filter(payment_method='cod')
        cod_count = Payment.objects.filter(payment_method='cod').count()
        cod_amount=0
        for cod in cod:
            print(type(cod.amount_paid))

        
        product=Product.objects.all()
        amount_of_stock=0
# price
# stock

        for prod in product:
            print('product price',prod.price)
            if prod.stock==0:
                continue
            else:
                print(prod.price,prod.stock)
                amount_of_stock+= prod.price * prod.stock
        print('________________________________________________',amount_of_stock)

        accepted=OrderProduct.objects.filter(status='Accepted').count()
        pending=OrderProduct.objects.filter(status='Pending').count()
        cancelled=OrderProduct.objects.filter(status='Cancelled').count()
        completed=OrderProduct.objects.filter(status='Completed').count()
        
        # cod_amount+=cod.amount_p    
        # print(sum_of_amount)
        # print(queryset)
        # print('/////////////////////////////',amount_cod)
        # print("haiiiii")
        # amount_paypal
        # amount_razorpay
        amount=razor_pay_amount+pay_pal_amount
        total_amount_recieved=razor_pay_amount+pay_pal_amount

        context={
            
            'sum_of_razor_paypayPal':sum_of_razor_paypayPal,
            'razor_pay_amount':razor_pay_amount,
            'pay_pal_amount':pay_pal_amount,
            'cod_amount':cod_amount,
            'cod_count':cod_count,
            'amount_of_stock':amount_of_stock,
            'amount': amount,
            'total_amount_recieved':total_amount_recieved,
            'accepted':accepted,
            'pending':pending,
            'cancelled':cancelled,
            'completed':completed,

        }

        return render(request,'adminpanel/index.html',context)

@never_cache
def userview(request):
    if request.session.get('logedin') !=True:
        return redirect('loginadmin')
    else:
        userdetails = Account.objects.all()
        paginator=Paginator(userdetails,6)
        page=request.GET.get('page')
        paginated_pages=paginator.get_page(page)
        
        return render(request, 'adminpanel/userview.html', {'userdata': paginated_pages})


def activeUser(request,id):
    if request.session.get('logedin') !=True:
        return redirect('loginadmin')
    else:
        status = Account.objects.get(id=id)
        if status.is_active:
            status.is_active = False
        else:
            status.is_active = True
        status.save()
        return redirect('userview')

@never_cache
def category(request):
    if request.session.get('logedin') !=True:
        return redirect('loginadmin')
    else:
        if request.method == 'POST':
            form = CategoryForms(request.POST)
            if form.is_valid():
                form.save()
                messages.info(request, 'added')
        forms = CategoryForms()
        context = {'form': forms,
                   'heading': 'Add category'}
        return render(request, 'adminpanel/printForms.html', context)

@never_cache
def viewcategory(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        cat_view = Category.objects.all()
        return render(request, 'adminpanel/viewcategory.html', {'catview': cat_view})
        
@never_cache
def edit_category(request,id):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        if request.method == 'POST':
            cat = Category.objects.get(id=id)
            form = CategoryForms(request.POST, instance=cat)
            if form.is_valid():
                form.save()
                return redirect('viewcategory')
        else:
            cat = Category.objects.get(id=id)
            form = CategoryForms(instance=cat)
            context = {'form': form,
                       'heading': 'Edit category'}
        return render(request, 'adminpanel/printForms.html', context)



def delete_category(request, id):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        categorylist = Category.objects.get(id=id)
        if Category.objects.filter(id=id).exists():
            categorylist.delete()
            return redirect("viewcategory")
        else:
            return redirect("viewcategory")

#product add
@never_cache
def add_product(request):

    

    if request.session.get('logedin') != True:
        return redirect('loginadmin')

    else:
       

        if request.method == 'POST':
            
            forms = ProductForms(request.POST,request.FILES)
            print(forms)
            
            # slug_test=request.POST['slug']
            # product_name_test=request.POST['product_name']
            # if Product.objects.filter(product_name=product_name_test,slug=slug_test).exists():
            #         print("hello existttting data")
            #         messages.info(request,'slug is already exist in database')
            #         return redirect('add_product')
            # forms = ProductForms(request.POST, request.FILES)
            # print('-----------------------------------------------------------method post')
        
            if forms.is_valid():
                print("asdasdasdas vaaalidddddd")
        

                product_name=forms.cleaned_data['product_name']

                category=forms.cleaned_data['category']
                slug=forms.cleaned_data['slug']
                description=forms.cleaned_data['description']
                brand=forms.cleaned_data['brand']
                price=forms.cleaned_data['price']
                stock=forms.cleaned_data['stock']
                image1 = request.POST['pro_img1']
                
                format, img1 = image1.split(';base64,')
                ext = format.split('/')[-1]
                img1_c = ContentFile(base64.b64decode(img1), name=product_name + '1.' + ext)
                
            
                image2 = request.POST['pro_img2']
            
            
                format, img2 = image2.split(';base64,')
                ext = format.split('/')[-1]
                img2_c = ContentFile(base64.b64decode(img2), name=product_name + '2.' + ext)

                

                image3 = request.POST['pro_img3']
                
                format, img3 = image3.split(';base64,')
                ext = format.split('/')[-1]
                img3_c = ContentFile(base64.b64decode(img3), name=product_name + '3.' + ext)
                    
                image4 = request.POST['pro_img4']
            
                format, img4 = image4.split(';base64,')
                ext = format.split('/')[-1]
                img4_c = ContentFile(base64.b64decode(img4), name=product_name + '4.' + ext)
                

                product_insert=Product(product_name=product_name,slug=slug,description=description,price=price,brand=brand,images1=img1_c,images2=img2_c,images3=img3_c,images4=img4_c,stock=stock,category=category)
                product_insert.save()
                forms = ProductForms()
                return redirect('view_product')
        else: 

            forms = ProductForms()       
            context = {'add_product_form': forms,
            'form_name':'ADD PRODUCT'}
            return render(request, 'adminpanel/productadd.html', context)

@never_cache
def view_product(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        product = Product.objects.all()
        return render(request, 'adminpanel/productview.html', {'products': product})



def delete_product(request, id):

    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:

        categorylist = Product.objects.get(id=id)
        if Product.objects.filter(id=id).exists():
            categorylist.delete()
            return redirect("view_product")
        else:
            return redirect("view_product")

@never_cache
def edit_product(request,id):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        if request.method == 'POST':
            cat = Product.objects.get(id=id)
            forms = ProductForms(request.POST, instance=cat)
            print('======================================',forms)
            if forms.is_valid():
                product_name=forms.cleaned_data['product_name']

                category=forms.cleaned_data['category']
                slug=forms.cleaned_data['slug']
                description=forms.cleaned_data['description']
                brand=forms.cleaned_data['brand']
                price=forms.cleaned_data['price']
                stock=forms.cleaned_data['stock']

                if request.POST['pro_img1']:

                    image1 = request.POST['pro_img1']

                    format, img1 = image1.split(';base64,')
                    ext = format.split('/')[-1]
                    img1_c = ContentFile(base64.b64decode(img1), name=product_name + '1.' + ext)
                    cat.images1=img1_c


                if request.POST['pro_img2']:

                    image2 = request.POST['pro_img2']

                    format, img2 = image2.split(';base64,')
                    ext = format.split('/')[-1]
                    img2_c = ContentFile(base64.b64decode(img2), name=product_name + '2.' + ext)
                    cat.images2=img2_c

                if request.POST['pro_img3']:

                    image3 = request.POST['pro_img3']
                    format, img3 = image3.split(';base64,')
                    ext = format.split('/')[-1]
                    img3_c = ContentFile(base64.b64decode(img3), name=product_name + '3.' + ext)
                    cat.images3=img3_c

                if request.POST['pro_img4']:

                    image3 = request.POST['pro_img3']
                    format, img3 = image3.split(';base64,')
                    ext = format.split('/')[-1]
                    img3_c = ContentFile(base64.b64decode(img3), name=product_name + '3.' + ext)
                    cat.images3=img3_c

                if request.POST['pro_img4']:

                    image4 = request.POST['pro_img3']

                    format, img4 = image4.split(';base64,')
                    ext = format.split('/')[-1]
                    img4_c = ContentFile(base64.b64decode(img4), name=product_name + '4.' + ext)
                    cat.images4 = img4_c

                cat.product_name=product_name
                cat.slug=slug
                cat.description=description
                cat.price=price
                cat.brand=brand 
                cat.stock=stock
                cat.category=category
                cat.save()
                
                return redirect('view_product')
        else:
            cat = Product.objects.get(id=id)
            form = ProductForms(instance=cat)
            context = {'add_product_form': form,
                       'heading': 'Edit category',
                        }
        return render(request, 'adminpanel/edit_product.html', context)


def order_details(request):

    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
    

        order_details=OrderProduct.objects.all().order_by('id')
        paginator=Paginator(order_details,6)
        page=request.GET.get('page')
        paginated_pages=paginator.get_page(page)
        forms=StatusForm()
        context={
            'order_details':paginated_pages,
            'forms':forms
        }
        

        return render(request,'adminpanel/orders_details.html',context)

# order status

def  order__product_status(request,id):

    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        order_detials_single=OrderProduct.objects.get(id=id)
        if request.method=='POST':
            forms=StatusForm(request.POST)
            if forms.is_valid():
                status= forms.cleaned_data.get("status")
                order_detials_single.status=status
                if order_detials_single.status=='Cancelled':
                    order_detials_single.product.stock=order_detials_single.product.stock+order_detials_single.quantity
                    order_detials_single.product.save()
                    order_detials_single.save()
                order_detials_single.save()
        return redirect('order_details')




# ADMIN PANEL report genaration

def report_genaration(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        return render(request,'adminpanel/report_genarations.html')


def month_report(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:
        if request.POST.get('month'):

            month=request.POST.get('month',False)
            
            print('fdhsdfhdshsdhsdhsdfhsdfhdshsh',month)
            x=[]
            x = month.split("-")
            print(x)
            mo=x[1]
            print('asdfasdfasdfsdfsd mooonth',mo)
            deliver=OrderProduct.objects.filter(status="Accepted",created_at__month=mo)
            print(deliver)
            total=0
            for delive in deliver:
                total+=delive.product_price
            context={
                'ordered':deliver,
                'total':total
            }
            
            return render(request,'adminpanel/monthly.html',context)
        else:

            return render(request,'adminpanel/report_genarations.html')


def yearly_report(request):

    # this is for session
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:

        if request.GET.get('year'):
            year=request.GET['year']
            print(year)
            total_order=OrderProduct.objects.filter(created_at__year=year,status='Accepted')

            total=0
            for price in total_order:
                total+=price.product_price
            context={
                'ordered':total_order,
                'total':total
            }
            return render(request,'adminpanel/monthly.html',context)
        else:
            return redirect('report_genaration')  


def date_report(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:


        if request.GET.get('start') and request.GET.get('end'):

            start=request.GET['start']           
            end=request.GET['end'] 

            total_order=OrderProduct.objects.filter(created_at__range=[start,end],status='Accepted')

            print(total_order)
            print(start,end) 
            total=0
            for delive in total_order:
                total+=delive.product_price
            context={
                'ordered':total_order,
                'total':total
            }

            return render(request,'adminpanel/monthly.html',context)
        else:
            return redirect('report_genaration')

# this is code for coupen view and adding coupen

def coupon_adding(request):


    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:

        if request.method== "POST":

            coupon_code=request.POST.get('coupon_code')
            discount=request.POST.get('discount')
            valid_from=request.POST.get('valid_from')
            valid_to=request.POST.get('valid_to')

            if Coupon_add.objects.filter(coupon_code=coupon_code).exists():

                coupon_adding = Coupon_add.objects.get(coupon_code = coupon_code)
            else: 

                coupon_adding = Coupon_add()
            
            coupon_adding.coupon_code= coupon_code
            coupon_adding.coupon_percentage= discount
            coupon_adding.coupon_start= valid_from
            coupon_adding.coupon_end= valid_to

            coupon_adding.save()
            




    
    return render(request,'adminpanel/coupen_adding.html')

def coupon_view(request):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:

        coupen_table=Coupon_add.objects.all()


        context={

            "coupen_table":coupen_table

                }

        return render(request,'adminpanel/coupon_view.html',context)


def coupon_delete(request,id):
    if request.session.get('logedin') != True:
        return redirect('loginadmin')
    else:

        offer=Coupon_add.objects.get(id=id)
        offer.delete() 
        return redirect('coupon_view')

def add_refferal_coupon(request):
    if request.method =='POST':
        ref_percentage=int(request.POST.get('percentege'))
        print(type(ref_percentage))
        refferal_coupon=RefferalCoupen.objects.all()
        for referels in refferal_coupon:
            referels.ref_percentage=ref_percentage
            referels.save()

    return render(request,'adminpanel/refferal_copon_adding.html')




# admin delete
def adminFlush(request):
    del request.session['logedin']
    return redirect('loginadmin')







# Create your views here.
