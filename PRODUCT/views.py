from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages

# Create your views here.
def products_list(request):
    products=Product.objects.all()
    return render(request,"product.html",locals())


def product_view(request,id):
    products=Product.objects.get(id=id)
    return render(request,"product_view.html",locals())


def add_product(request):
    if request.method == "POST":
        product_id=request.POST.get("product_id")
        name=request.POST.get("name")
        price=request.POST.get("price")
        category=request.POST.get("category")
        stock=request.POST.get("stock")
        description=request.POST.get("description")
        image=request.FILES.get("image")

        product=Product.objects.filter(product_id=product_id)
        if product:
            messages.warning(request,"Already have product with this id!")
            return redirect('add_product')
        else:
            product=Product.objects.create(
                product_id=product_id,
                name=name,
                price=price,
                category=category,
                stock=stock,
                description=description,
                image=image
            )
            product.save()
            messages.success(request,"Product added succesfully!")
            return redirect('products_list')
    return render(request,"add_product.html",locals())
