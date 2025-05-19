from django.db import models

# Create your models here.
class Customer(models.Model):
    fullname=models.CharField(max_length=255)
    phone=models.IntegerField(unique=True)
    address=models.TextField()

    def __str__(self):
        return self.fullname
    
