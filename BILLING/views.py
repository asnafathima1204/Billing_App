from django.shortcuts import render,redirect
from BILLING.models import *
from django.contrib import messages
from decimal import Decimal
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

# Create your views here.
def invoices(request):
    invoices=Invoice.objects.all()
    return render(request,"invoices.html",locals())

def create_invoice(request):
    customers=Customer.objects.all()
    products=Product.objects.all()
    phone=request.session.get("phone")
    customer = None
    total = 0

    
    if phone:
        try:
            customer=Customer.objects.get(phone=phone)
        except Customer.DoesNotExist:
            messages.error(request, "Customer not found. Please select a valid customer.")
            return redirect('create_invoice')
    
    if request.method == "POST":
        if not customer:
            messages.error(request, "No customer selected. Please select a customer.")
            return redirect('create_invoice')
        
        
        products = request.POST.getlist("products[]")
        if not products:
            messages.error(request,"Did you forget to select the product?")
            return redirect('create_invoice')
            
        invoice=Invoice.objects.create(customer=customer)
        qtys = request.POST.getlist("qty[]")

        for i in range(len(products)):
            product=Product.objects.get(id=products[i])
            sub_total = product.price * Decimal(qtys[i])
            print(invoice)
            invoiceItem=InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=qtys[i],
                sub_total=sub_total
            )

            total += invoiceItem.sub_total
            invoice.total = total
            tax = total * (Decimal(invoice.gst_percentage/100))
        
        grand_total = total + tax
        invoice.grand_total = grand_total
        invoice.save()
        del request.session['phone']
        messages.success(request,"Invoice created succesfully")
        return redirect('invoices')

       
    return render(request,"create_invoice.html",locals())



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

    tax = invoice.total * Decimal(invoice.gst_percentage/100)
    return render(request,"view_invoice.html",locals())


def render_to_pdf(html_page,context):
    template = get_template(html_page)
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    pisa_status = pisa.CreatePDF(html, dest = response)


    return response if not pisa_status.err else HttpResponse('Error creating pdf')

def invoice_pdf(request,id):
    invoice=Invoice.objects.get(id=id)
    invoice_item = InvoiceItem.objects.filter(invoice=invoice)
    gst = Decimal(invoice.gst_percentage/100)
    tax = invoice.total * gst


    context={
        'invoice':invoice,
        'invoice_item':invoice_item,
        'tax':tax
    }
    return render_to_pdf("invoice_pdf.html",context)