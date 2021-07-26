from django.db import models
from store.models import Product
from accounts.models import Account


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    # user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    user=models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE,null=True)   
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.product


    def sub_total(self):
        
        if self.product.product_offer_price:

            return self.product.product_offer_price * self.quantity

        elif self.product.category_offer_price:
            
            return self.product.category_offer_price * self.quantity

        else:
            return self.product.price * self.quantity
            

    # def sub_total(self):
    #     return self.product.price * self.quantity

    # def __unicode__(self):
    #     return self.product
