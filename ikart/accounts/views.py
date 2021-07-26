
from django.contrib import messages,auth
from django.contrib import messages
from django.contrib.auth import decorators
from django.core.exceptions import ObjectDoesNotExist
from django.http import request
from django.http.response import HttpResponse
from django.shortcuts import render
from django.shortcuts import render,redirect
from .forms import RegistrationForms
from .models import *
from django.contrib.auth.decorators import login_required
from twilio.rest import Client
from  django.contrib.sessions.models import Session
from django.contrib import messages
from cart.views import _cart_id
from cart.models import Cart,CartItem
from order.models import *
from django.http import JsonResponse
import json

import random


# Verification email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# this is fro url redirecting
import requests
from accounts.utils import genarate_ref_code

# profile image
from django.core.files.base import ContentFile
import base64




def register(re,recomended_code=None):


    # re.session['recomended_code']=recomended_code
    # print(re.session['recomended_code'],'ith sessionilaaan')

    # referal_code parameter is deining about the recommended uuer
    # print('this is referal code from the request',referel_code)

    code=genarate_ref_code()
    
    # try:
    #     a=Refferal_user()
    #     print(a)
    # except:
    #     pass
   
    # if referel_code:
    #     # print("referal value is defined in the true functions")

    if re.method=='POST':
       
        form=RegistrationForms(re.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone_number = form.cleaned_data['phone_number']
            email= form.cleaned_data['email']
            password= form.cleaned_data['password']
            username=email.split('@')[0]
            user=Account.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.phone_number=phone_number
            user.save()

            
            # user
            # code
            # recomended_by

            # if the user login by recomndation
            if recomended_code:
                
                
                
                refered_by=Refferal_user.objects.get(code=recomended_code)
                print(refered_by,'--------------------------------------------')
                new_user=Refferal_user()
                new_user.user=user
                new_user.code=code
                print(refered_by)
                new_user.recomended_by=refered_by.user
                new_user.save()

                # referal coupon creations
                # referd user coupon
                ref_coupon= RefferalCoupen()
                ref_user_code=genarate_ref_code()
                ref_copon_code="REF"+ref_user_code

                ref_coupon.user=refered_by.user
                ref_coupon.ref_coupon=ref_copon_code
                ref_coupon.ref_percentage=10
                ref_coupon.save()

                # new user coupon
                newusr_coupon=RefferalCoupen()
                ref_new_code=genarate_ref_code()

                new_user_coupon="NEW"+ref_new_code

                newusr_coupon.user=user
                newusr_coupon.ref_coupon=new_user_coupon
                newusr_coupon.ref_percentage=10
                newusr_coupon.save()
                
            

            else:
            # if the user is not register with Refferal
            # then manke the user database with referal code 
            # and saved in refferal user database 

                new_user=Refferal_user()
                new_user.user=user
                new_user.code=code
                new_user.save()
                print(new_user.user)     
        

            
            messages.success(re,'registration success')
            return redirect('login')
    else:
        form = RegistrationForms()
    context={
        'form':form,
    }
    return render(re,'accounts/register.html',context)

def login(request):

    if request.user.is_authenticated:
        return redirect('index1')
    
    else:
        
        if request.method=="POST":
            email=request.POST['mail']
            password=request.POST['password']
            user=auth.authenticate(email=email,password=password)
            if user is not None:
                try:

                    cart=Cart.objects.get(cart_id=_cart_id(request))
                    is_cart_item_exist=CartItem.objects.filter(cart=cart).exists()
                    if is_cart_item_exist:
                        cart_items=CartItem.objects.filter(cart=cart)
                        for items in cart_items:
                            items.user=user
                            items.save()
                            # print('user saved',items.user)
                except:
                    # print("passed to except block")
                    pass

                
                auth.login(request,user)
                # messages.success(re,"your succesfully created")
                url=request.META.get('HTTP_REFERER')

                try:
                    query = requests.utils.urlparse(url).query
                    # next=/cart/checkout/
                    params = dict(x.split('=') for x in query.split('&'))
                    if 'next' in params:
                        nextPage = params['next']
                        return redirect(nextPage)
                except:

                    return redirect('index1')

            else:
                messages.info(request,'credential is not correct')
                return redirect('login')
        return render(request,'accounts/login.html')



def otp_generate(request):

    if request.method =='POST':
        phonenumber=request.POST['phonenumber']
        
        if Account.objects.filter(phone_number=phonenumber).exists():
            otp = random.randint(100000,999999)
            otp=str(otp)
            account_sid ='AC45a51315690af834c14f6f59ee6d8187'
            auth_token ='d7d9f26cdcb5d3581f173ed9e290bdea'
            client=Client(account_sid,auth_token)
            message = client.messages \
                .create(
                     body="Yourlogin OTP "+otp,
                     from_='+12202001892',
                     to='+91'+phonenumber
                 )
            request.session['otp']=otp
            request.session['phonenumber']=phonenumber 
            messages.success(request,'message sended')
            return redirect('otp_generate')
        messages.error(request,'Enter a registerd number')
        return redirect('otp_generate')
    return render(request,'accounts/otp.html')


def otp_checking(request):


    if request.method =='POST':
        otpnumber=request.POST['otpnumber']

        if request.session.has_key('otp'):
            user_otp=str(request.session['otp'])

            if otpnumber==user_otp:
                phonenumber=request.session['phonenumber']
                userdtls=Account.objects.get(phone_number=phonenumber)
                auth.login(request,userdtls)
                del request.session['otp']
                del request.session['phonenumber']
                return redirect('index1')
            
            else:
                messages.error(request,'otp is not valid')
        
        else:
            return redirect('otp_generate')
    
    else:
        messages.error(request,'please ente the registerd number')
        return redirect('otp_generate')
# forgot password

def forgott_password(request):

    if request.method=='POST':
        email=request.POST.get('mail',False)
        print("form",email)
        email1=Account.objects.filter(email=email)
        print(email1)
        
        if Account.objects.filter(email=email).exists():
            user=Account.objects.get(email__iexact=email)

            # reset password from mail
            current_site=get_current_site(request)
            mail_subject="Reset Your password"
            message=render_to_string('accounts/reset_password_email.html',{
                'user':user,
                'domain':current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':default_token_generator.make_token(user),
            })
            to_email=email
            send_email=EmailMessage(mail_subject,message,to=[to_email])
            send_email.send()
            messages.success(request,'Password reset email has been sent your email address')
            return redirect('login')

        else:
            messages.error(request,'Account Does not exists')
            return redirect('forgott_password')
            
    return render(request,'accounts/forgott_password.html') 

def reset_password_validate(request,uidb64,token):
     
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):

        request.session['uid']=uid
        messages.success(request,'please reset your password')
        return redirect('reset_password')
    
    else:

        messages.error(request,'this link has been expired')
        return redirect('login')
    
# this function is after the email recieved
def reset_password(request):

# create_password
# confirm_password
    if request.method=="POST":
        created_password=request.POST.get('create_password')
        confirm_password=request.POST.get('confirm_password')

        print('created_password',created_password,'confirm password',confirm_password)
        

        if created_password == confirm_password:
            uid=request.session.get('uid')
            user=Account.objects.get(id=uid)
            print(user.first_name)
            user.set_password(created_password)
            user.save()
            messages.success(request,'succesfully changed the password')
            return redirect('login')

        else:
            messages.error(request,'password is not match')
            redirect('reset_password')
    else:
        return render(request,'accounts/reset_password.html')

    
@login_required(login_url='login')
def signout_user(re):

    auth.logout(re)
    messages.success(re,'logiedin')
    return redirect('index1')

def user_profile(request):
    print("haidddd")

    try:
        # print("hai")
        refferal_link_code=Refferal_user.objects.get(user=request.user)
        refferal_coupon=RefferalCoupen.objects.filter(user=request.user)
        
        code=refferal_link_code.code
        refferal_link='http://127.0.0.1:8000/accounts/register/'+code
        print(refferal_link)
        print('this is tthe code for user',code)
        # print(refferal_coupon,"this is refferal coupon")
        
    except:
        pass


    order_product=OrderProduct.objects.filter(user=request.user)
    user=request.user

    try:
        address=Account.objects.get(email=user)
        if UserProfile.objects.filter(user=request.user).exists():
            profile_images= UserProfile.objects.get(user=request.user)
        else:
            profile_images=None


        
        context={
            'address':address,
            'order_product':order_product,
            'refferal_coupon':refferal_coupon,
            'refferal_link':refferal_link,
            'profile_images':profile_images,

             }
        return render(request,'accounts/user_profile.html',context)

    except ObjectDoesNotExist:

        messages.info(request,"please add address")
        return render(request,'accounts/user_profile.html')
 
    
   
    # address1=address[0]

  
def collect_address(request):

    if request.method == "GET":
        id=request.GET['address']
        print(id)
        add=UserAddress.objects.get(id=id)
        print(add.last_name)

        data = {}
        data['first_name']=add.first_name
        data['last_name']=add.last_name
        data['phone']=add.phone
        data['email']=add.email
        data['address1']=add.address_line1
        data['address2']=add.address_line2
        data['city']=add.city
        data['state']=add.state

        return HttpResponse(json.dumps(data), content_type="application/json")

# profile address edit function

def collect_address_user(request):


        if request.method == "GET":
            id=request.GET['address']

            add=UserAddress.objects.get(id=id)
            

            data = {}
            data['first_name']=add.first_name
            data['last_name']=add.last_name
            data['phone']=add.phone
            data['email']=add.email
            data['address1']=add.address_line1
            data['address2']=add.address_line2
            data['city']=add.city
            data['state']=add.state

        return HttpResponse(json.dumps(data), content_type="application/json")

def view_address(request):

    user=request.user
    addresses=UserAddress.objects.filter(user=user)
    context={
        'addresses':addresses
    }
    return render(request,'accounts/address_add.html',context)

def save_address(request):

    print('hello')
    
    data= request.POST

    user_address= UserAddress()
            

    if UserAddress.objects.filter(first_name=data['first_name'],last_name=data['last_name'],phone=data['phone'],email=data['email'],address_line1=data['address_line_1'],address_line2=data['address_line_2'],state=data['state'],city=data['city'],user=request.user.id).exists():
            messages.error(request,'address already exist')
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
        messages.success(request,'succesfully saved')


    return redirect('view_address')


# delete address

def delete_address(request,address_id):

    single_address=UserAddress.objects.get(id=address_id)
    single_address.delete()
    messages.success(request,'deleted ')
    return redirect('view_address') 

def edit_address(request,address_id ):
    address=UserAddress.objects.get(id=address_id)

    if request.method=='POST':

        addres=UserAddress.objects.get(id=address_id)

        data=request.POST

        addres.user=request.user

        addres.first_name=data['first_name']
        
        addres.last_name=data['last_name']

        addres.phone=data['phone']

        addres.email=data['email']

        addres.address_line1=data['address_line_1']

        addres.address_line2=data['address_line_1']

        addres.city=data['city']

        addres.state=data['state']

        addres.save()
        messages.success(request, ' updated ')

        return redirect('view_address')




    context={
        'address':address

    }

    return render(request,'accounts/edit_address.html',context)


def user_images(request):
    if request.method=='POST':
        

        # user
        # image
        name=request.user.first_name
        image1 = request.POST['pro_img1']
        format, img1 = image1.split(';base64,')
        ext = format.split('/')[-1]
        img1_c = ContentFile(base64.b64decode(img1), name=name + '1.' + ext)

        if UserProfile.objects.filter(user=request.user):
            user_profile=UserProfile.objects.get(user=request.user)
        else:
            user_profile=UserProfile()
        
        user_profile.user=request.user
        user_profile.image=img1_c
        user_profile.save()

        return redirect('user_profile')
    


        
        






        