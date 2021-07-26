from django import forms
from django.db.models.base import Model
from django.forms import ModelForm
from django.forms.widgets import Textarea
from category.models import Category
from store.models import Product
from order.models import Order

class CategoryForms(ModelForm):
    class Meta:
        model=Category
        fields= '__all__'
    def __init__(self, *args, **kwargs):

        # first call parent's constructor
        super().__init__(*args, **kwargs)
        self.fields['category_name'].widget.attrs.update({'class': ' text-white form-control rounded-0 col-11'})
        self.fields['description'].widget.attrs.update({'class': ' text-white form-control rounded-0 col-11'})
        self.fields['slug'].widget.attrs.update({'class': ' text-white form-control rounded-0 col-11'})

class ProductForms(forms.ModelForm):
    class Meta:
        model = Product
        fields =  ['product_name','slug','description','price','brand','images1','images2','images3','images4','stock','is_available','category']














        # widgets = {
        #     'name': Textarea(attrs={
        #         'class': "form-control",
        #         'style': 'max-width: 200px;',
        #         'placeholder': 'Name'
        #         })
        #     # 'email': EmailInput(attrs={
        #     #     'class': "form-control", 
        #     #     'style': 'max-width: 300px;',
        #     #     'placeholder': 'Email'
        #     #     })
        # }
    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super().__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['images2'].required = True
        self.fields['images3'].required = True
        self.fields['images4'].required = True
        self.fields['description'].widget.attrs.update({'class': ' text-white form-control rounded-0 col-11'})
        self.fields['price'].widget.attrs.update({'class': 'text-white form-control rounded-0 col-11'})
        self.fields['brand'].widget.attrs.update({'class': 'text-white form-control rounded-0 col-11'})
        self.fields['stock'].widget.attrs.update({'class': 'text-white form-control rounded-0 col-11'})
        self.fields['category'].widget.attrs.update({'class': 'text-white form-control rounded-0 col-11'})
        self.fields['slug'].widget.attrs.update({'class': 'text-white form-control rounded-0 col-11'})
        self.fields['product_name'].widget.attrs.update({'class': 'text-white form-control rounded-0 col-11'})
        self.fields['images1'].widget.attrs.update({'class': ' btn btn-outline-dark  col-11'})
        self.fields['images2'].widget.attrs.update({'class': ' btn btn-outline-dark col-11'})
        self.fields['images3'].widget.attrs.update({'class': ' btn btn-outline-dark col-11'})
        self.fields['images4'].widget.attrs.update({'class': ' btn btn-outline-dark col-11'})
        # self.fields['images1'].label = ""


        

# class NewProductForm(forms.ModelForm):
#     class Meta:
#         model = product
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(NewProductForm, self).__init__(*args, **kwargs)
#         self.fields['product_name'].widget.attrs['placeholder'] = 'Enter name of the product'
#         self.fields['slug'].widget.attrs['placeholder'] = 'Enter slug name'
#         self.fields['description'].widget.attrs['placeholder'] = 'Add discription'
#         self.fields['price'].widget.attrs['placeholder'] = 'Price per unit'
#         self.fields['stock'].widget.attrs['placeholder'] = 'Number of stock available'
#         self.fields['brand'].widget.attrs['placeholder'] = 'Brand Name'
#         self.fields['Images'].widget.attrs['onchange'] = 'readURL(this)'
#         self.fields['Images11'].widget.attrs['onchange'] = 'readURL11(this)'
#         self.fields['Images22'].widget.attrs['onchange'] = 'readURL22(this)'
#         for field in self.fields:
#             self.fields[field].widget.attrs['class'] = 'form-control'
