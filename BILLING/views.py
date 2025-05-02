from django.shortcuts import render

# Create your views here.
def billing_list(request):
    return render(request,"billing.html")
