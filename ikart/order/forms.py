from django import forms
from django.db.models import fields
from django.forms import ModelForm, widgets
from .models import *


class OrderForm(forms.ModelForm):
    class Meta:
        model=Order
        fields=['first_name','last_name','phone','email','address_line1','address_line2','state','city','order_note']
        
        
class StatusForm(ModelForm):
    class Meta:
        model=Order
        fields = ['status'] 
# CategoryOffer
# ProductOffer

class CategoryForm(ModelForm):
    class Meta:
        model=CategoryOffer
        fields= '__all__'
    