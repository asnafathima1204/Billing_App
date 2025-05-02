from django.db import models

# Create your models here.
class Product(models.Model):
    product_id=models.CharField(max_length=10)
    name=models.CharField(max_length=255)
    description=models.TextField(null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.PositiveIntegerField()
    image=models.ImageField(upload_to='products/',null=True,blank=True)
    category=models.CharField(max_length=255,null=True,blank=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



