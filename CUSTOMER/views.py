from django.shortcuts import render
from CUSTOMER.models import *
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def customers(request):
    customers=Customer.objects.all().order_by('-id')
    return render(request,"customers.html",locals())

