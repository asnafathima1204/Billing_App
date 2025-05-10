from django.shortcuts import render
from CUSTOMER.models import *

# Create your views here.
def customers(request):
    customers=Customer.objects.all()
    return render(request,"customers.html",locals())

