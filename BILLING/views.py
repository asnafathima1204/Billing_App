from django.shortcuts import render,redirect
from BILLING.models import *
from django.contrib import messages

# Create your views here.
def invoices(request):
    invoices=Invoice.objects.all()
    return render(request,"invoices.html",locals())

def create_invoice(request):
    customers=Customer.objects.all()
    products=Product.objects.all()
    phone=request.session.get("phone")
    if phone:
        customer=Customer.objects.get(phone=phone)
        del request.session['phone']
        print(customer)


    if request.method == "POST":
        pass
    return render(request,"create_invoice.html",locals())

def invoice_product(request):
    # if request.method
    return redirect('create_invoice.html')

def new_customer(request):
    if request.method == "POST":
        fullname=request.POST.get("fullname")
        phone=request.POST.get("phone")
        address=request.POST.get("address")

        customer=Customer.objects.create(
            fullname=fullname,
            phone=phone,
            address=address
        )
        

        customer.save()
        messages.success(request,"New Customer Added Successfully")
        return redirect('create_invoice')
    
    return redirect('create_invoice')

def existing_customer(request):
    if request.method == "POST":
        phone=request.POST.get("phone")
        request.session['phone'] = phone
        return redirect('create_invoice')
    return redirect('create_invoice')


def view_invoice(request,id):
    invoice=Invoice.objects.get(id=id)
    invoiceItem=InvoiceItem.objects.filter(invoice=invoice)
    total=0

    for item in invoiceItem:
        item.sub_total = item.quantity * item.product.price
        total += item.sub_total

    from decimal import Decimal
    tax = total * (Decimal(invoice.gst_percentage) / Decimal(100))

    invoice.grand_total = total + tax
    invoice.save()


    return render(request,"view_invoice.html",locals())
