from django.shortcuts import render,redirect
from .models import *
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def products_list(request):
    if request.method == "GET":
        search=request.GET.get("search")
        print(search)
        if search:
            products=Product.objects.filter(
                Q(name__icontains=search)|
                Q(category__icontains=search)|
                Q(product_id__icontains=search))
        else:
            products=Product.objects.all()
    return render(request,"product.html",locals())


@login_required
def product_view(request,id):
    product=Product.objects.get(id=id)
    return render(request,"product_view.html",locals())


@login_required
def add_product(request):
    if request.method == "POST":
        product_id=request.POST.get("product_id")
        name=request.POST.get("name")
        price=request.POST.get("price")
        category=request.POST.get("category")
        stock=request.POST.get("stock")
        description=request.POST.get("description")
        image=request.FILES.get("image")
        if int(stock) < 0:
            messages.warning(request,"Stock can't be less than zero")
            return redirect('add_product')
        
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
            
            )
            if image:
                product.image=image
                product.save()
            

            messages.success(request,"Product added succesfully!")
            return redirect('products_list')
    return render(request,"add_product.html",locals())


@login_required
def update_product(request,id):
    product=Product.objects.get(id=id)
    if request.method == "POST":
        product.name=request.POST.get("name")
        product.price=request.POST.get("price")
        product.category=request.POST.get("category")
        stock=request.POST.get("stock")
        product.description=request.POST.get("description")
        if int(stock) < 0:
            messages.warning(request,"Product can't be less than  zero")
            return redirect('update_product', id=id)
        product.stock = stock
        
        new_image=request.FILES.get("image")
        if new_image:
            product.image=new_image


        product.save()
        messages.success(request,"Product updated successfully")
        return redirect('product_view',id=id)
    return render(request,"update_product.html",locals())


@login_required
def del_product(request,id):
    product=Product.objects.get(id=id)
    product.delete()
    return redirect('products_list')

