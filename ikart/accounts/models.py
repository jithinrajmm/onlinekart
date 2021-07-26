

from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
from django.db.models.deletion import CASCADE
from .utils import genarate_ref_code


class MyAccountManager(BaseUserManager):

    def create_user(self,first_name,last_name,username,email,password=None):
        if not email:
            raise ValueError("email is must enter")
        if not username:
            raise ValueError('user name is mandatory')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name
        )

        user.set_password(password)
        
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,email,username,password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        is_admin = models.BooleanField(default=True)
        is_staff = models.BooleanField(default=True)
        is_active = models.BooleanField(default=True)
        is_superadmin = models.BooleanField(default=True)
        user.save(using=self._db)
        return user
        
class Account(AbstractBaseUser):

    first_name=models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=50)
    #required
    date_joined=models.DateTimeField(auto_now_add=True)
    last_login =models.DateTimeField(auto_now_add=True)
    is_admin=models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username','first_name','last_name']
    
    objects=MyAccountManager()
    def __str__(self):
        return self.email
    def has_perm(self,perm,obj=None):
        return self.is_admin
    def has_module_perm(self,add_label):
        return True


# User address model

class UserAddress(models.Model):

    user=models.ForeignKey(Account,on_delete=models.CASCADE)  
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    phone=models.CharField(max_length=50)
    email=models.EmailField(max_length=50)
    address_line1=models.CharField(max_length=50)
    address_line2=models.CharField(max_length=50,blank=True)

    city=models.CharField(max_length=50)
    state=models.CharField(max_length=50)  


    def __str__(self):
        return self.first_name 


class Refferal_user(models.Model):
    
    user=models.OneToOneField(Account,on_delete=models.CASCADE,)
    bio=models.TextField(blank=True)
    code=models.CharField(max_length=12,blank=True)
    recomended_by=models.ForeignKey(Account,on_delete=models.CASCADE,blank=True, null=True, related_name='user')
    updated=models.DateTimeField(auto_now=True) 
    created=models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f"{self.user.username}-{self.code}"


    def get_recomended_profiles(self):
        pass

class RefferalCoupen(models.Model):
    
    user=models.ForeignKey(Account,on_delete=models.CASCADE)
    ref_coupon= models.CharField(max_length=20)
    ref_percentage=models.IntegerField(null=True)

    def __str__(self):
        return self.user



    # def save(self,*args,**kwargs):
    #     if self.code=="":
    #         code = genarate_ref_code
    #         self.code=code
    #     super().save(*args,**kwargs)

# this model is used to store the image of user

class UserProfile(models.Model):

    user=models.OneToOneField(Account,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='profileimages/',null=True,blank=True)
    
    def __str__(self):
        return self.user


