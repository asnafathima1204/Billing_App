from django.shortcuts import render
from CUSTOMER.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.
@login_required
def customers(request):
    customers=Customer.objects.all().order_by('-id')
    if request.method == "GET":
        search=request.GET.get("search")
        customer=Customer.objects.all().order_by('-id')
        if search:
            customers=Customer.objects.filter(Q(fullname__icontains=search)|Q(id__icontains=search)|Q(phone__icontains=search))
         
        else:
            customers=Customer.objects.all().order_by('-id')
    return render(request,"customers.html",locals())

