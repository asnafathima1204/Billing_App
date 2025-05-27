from django.db import models
from CUSTOMER.models import *
from PRODUCT.models import *
from django.contrib.auth.models import User

# Create your models here.
class Invoice(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    staff=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    gst_percentage=models.IntegerField(default=2)
    gst=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    total = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    grand_total=models.DecimalField(max_digits=15,default=0,decimal_places=2)

    def __str__(self):
        return f"Invoice {self.id}"
    
    
class InvoiceItem(models.Model):
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    sub_total = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def __str__(self):
        return f"Invoice: {self.invoice}"


     

class Cart(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    total=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    gst_percentage=models.IntegerField(default=2)
    gst=models.DecimalField(max_digits=5,decimal_places=2,default=0.00)
    grand_total=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def __str__(self):
        return f"Cart No: {self.id}"




class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField(default=1)
    sub_total=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)

    def __str__(self):
        return f"Cart {self.cart.id}"





    

