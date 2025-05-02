from django.db import models
from CUSTOMER.models import *
from PRODUCT.models import *

# Create your models here.
class Invoice(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True)
    invoice_no=models.CharField(unique=True)

    def __str__(self):
        return f"Invoice {self.invoice_number}"
    
class InvoiceItem(models.Model):
    invoice=models.ForeignKey(Invoice,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    total=models.IntegerField()

    def __str__(self):
        return self.invoice.fullname





    

