from django.db import models
from decimal import Decimal

# Create your models here.
class Customer(models.Model):
    fullname=models.CharField(max_length=255)
    phone=models.IntegerField(unique=True)
    address=models.TextField()
    wallet=models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('1000.00'))

    def __str__(self):
        return self.fullname
    
