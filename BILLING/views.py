from django.shortcuts import render,redirect
from BILLING.models import *
from django.contrib import messages
from decimal import Decimal
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models import Q
from datetime import datetime
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def invoices(request):
    if 'phone' in request.session:
        del request.session['phone']
    if request.method == "GET":
        search=request.GET.get("search")
        date=request.GET.get("date")
        invoices=Invoice.objects.all().order_by('-id')
        if search:
            invoices=Invoice.objects.filter(Q(customer__fullname__icontains=search)|Q(id__icontains=search)|Q(grand_total__icontains=search))
           

        elif date:
            invoices=Invoice.objects.filter(date__date=date)

        else:
            invoices=Invoice.objects.all().order_by('-id')
    return render(request,"invoices.html",locals())



@login_required
def create_invoice(request):
    phone = request.session.get("phone")
    customers = Customer.objects.all()
    cart = request.session.get('cart',[])
   
    # If phone in session, get the customer object
    if phone:
        customer = Customer.objects.filter(phone=phone).first()

    search=request.GET.get("search_product")
    if search:
            products=Product.objects.filter(Q(name__startswith=search) & Q(stock__gt=0))
            if not products.exists():
                messages.error(request, "Requested product not found!")
            
    

    


    

    # GET request: just render the invoice creation page
    return render(request, "create_invoice.html", locals())


# @login_required
# def search_product(request):
#     # if request.method == "GET":
#     #     search=request.GET.get("search_product")
#     #     if search:
#     #         try:
#     #             search_products=Product.objects.filter(name__icontains=search)
#     #             print(search_products)
#     #             return redirect('create_invoice')
#     #         except:
#     #             messages.error(request,"Invalid product")
#     #             return redirect('create_invoice')
#     #     else:
#     #         messages.error(request,"do you forget to search product")
#     #         return redirect('create_invoice')


#     return redirect('create_invoice')


@login_required
def new_customer(request):
    if request.method == "POST":
        fullname=request.POST.get("fullname")
        phone=request.POST.get("phone")
        address=request.POST.get("address")

        customer=Customer.objects.filter(phone=phone)
        if not customer:
            Customer.objects.create(
                fullname=fullname,
                phone=phone,
                address=address
            )

            request.session['phone'] = phone

            messages.success(request,"New Customer Added Successfully")
            return redirect('create_invoice')
        else:
            messages.warning(request,"Already have customer with this number")
            return redirect('create_invoice')
    
    return redirect('create_invoice')

@login_required
def search_cutomer(request):
    customer=None
    if request.method == "GET":
        search = request.GET.get("search")
        if search:
            try:
                customer=Customer.objects.get(phone=search)
                print(customer)
                request.session['phone']=search
                return redirect('create_invoice')
            except:
                messages.error(request,"Customer not found with this number")
                return redirect('create_invoice')
        else:
            messages.error(request,"Customer not found with this number")
            return redirect('create_invoice')
    return redirect('create_invoice')



@login_required
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
        'request': request,
        'invoice':invoice,
        'invoice_item':invoice_item,
        'tax':tax
    }
    return render_to_pdf("invoice_pdf.html",context)


