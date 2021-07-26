from accounts.models import Account
from django.db import models
from category.models import Category
from django.urls import reverse
from datetime import date

#product table

class Product(models.Model):
    product_name = models.CharField(max_length=100,unique=True)
    slug         = models.SlugField(max_length=200,unique=True)
    description  = models.TextField(max_length=500,blank=True)
    price        = models.IntegerField()
    brand          = models.CharField(max_length=100,default=None)
    images1       = models.ImageField(upload_to='productimages/')
    images2 = models.ImageField(upload_to='productimages/',blank=True)
    images3 = models.ImageField(upload_to='productimages/',blank=True)
    images4 = models.ImageField(upload_to='productimages/',blank=True)
    stock        = models.IntegerField()
    is_available  = models.BooleanField(default=True)
    category      =models.ForeignKey(Category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date =models.DateTimeField(auto_now=True)

    product_offer_price=models.FloatField(null=True)
    offer_percentage=models.FloatField(null=True)
    category_offer_price=models.FloatField(null=True)
    
    def get_url(self):

        return reverse('product_details', args=[self.category.slug,self.slug])


    def __str__(self):
        return self.product_name
# Create your models here.


class CategoryOffer(models.Model):

    category=models.OneToOneField(Category,on_delete=models.CASCADE)
    offer=models.IntegerField()
    offer_start=models.DateField()
    offer_end=models.DateField()


    def check_expired(self):
        today = date.today()
        today1 = today.strftime("%Y-%m-%d")
        if str(self.offer_end)<= today1:
            return False
        else:
            return True   


class ProductOffer(models.Model):

    product=models.OneToOneField(Product,on_delete=models.CASCADE)
    offer=models.IntegerField()
    offer_start=models.DateField()
    offer_end=models.DateField()



    def check_expired(self):
        today = date.today()
        today1 = today.strftime("%Y-%m-%d")
        if str(self.offer_end)<= today1:
            return False
        else:
            return True 


class ReviewRating(models.Model):

    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    subject=models.CharField(max_length=100,blank=True)
    review=models.CharField(max_length=500,blank=True)
    rating=models.FloatField()
    ip=models.CharField(max_length=100,blank=True)
    status=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject


class Coupon_add(models.Model):

    coupon_code=models.CharField(max_length=20)
    coupon_percentage=models.IntegerField()
    coupon_start=models.DateField()
    coupon_end =models.DateField()

    def expire_date(self):
        today=date.today()
        todays=today.strftime("%Y-%m-%d")
        if str(self.coupon_end)< todays:
            return False
        else:
            return True

class UsedOffer(models.Model):

    
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    coupen=models.ForeignKey(Coupon_add,on_delete=models.CASCADE) 
    is_orderd=models.BooleanField(default=False)        
