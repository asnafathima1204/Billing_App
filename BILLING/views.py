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
        invoices=Invoice.objects.all()
        if search:
            invoices=Invoice.objects.filter(Q(customer__fullname__icontains=search)|Q(id__icontains=search)|Q(grand_total__icontains=search))
           

        elif date:
            invoices=Invoice.objects.filter(date__date=date)

        else:
            invoices=Invoice.objects.all()
    return render(request,"invoices.html",locals())

# @login_required
# def create_invoice(request):
#     phone= phone=request.session.get("phone")
#     customers=Customer.objects.all()
#     products=Product.objects.filter(stock__gt=0).order_by('name')
#     customer = None
#     total = 0
#     if not phone:
#         # messages.error(request, "No customer phone number provided.")
#         return render(request, "create_invoice.html", locals())
    
#     customer = Customer.objects.filter(phone=phone).first()
#     if not customer:
#         messages.error(request, "Customer not found. Please select a valid customer.")
#         return render(request, "create_invoice.html", locals())
    
#     if request.method == "POST":
#         if not customer:
#             messages.error(request, "No customer selected. Please select a customer.")
#             return redirect('create_invoice')
        
        
#         products = request.POST.getlist("products[]")
#         if not products:
#             messages.error(request,"Did you forget to select the product?")
#             return redirect('create_invoice')
            
#         invoice=Invoice.objects.create(customer=customer,staff=request.user)
#         qtys = request.POST.getlist("qty[]")

#         for i in range(len(products)):
#             product=Product.objects.get(id=products[i])
#             sub_total = product.price * Decimal(qtys[i])
#             print(invoice)
#             invoiceItem=InvoiceItem.objects.create(
#                 invoice=invoice,
#                 product=product,
#                 quantity=qtys[i],
#                 sub_total=sub_total
#             )
            
#             product.stock -= int(invoiceItem.quantity)
#             product.save()
#             total += invoiceItem.sub_total
#         invoice.total = total
#         tax = total * (Decimal(invoice.gst_percentage/100))
        
#         grand_total = total + tax
#         invoice.grand_total = grand_total
#         invoice.save()
#         del request.session['phone']
#         messages.success(request,"Invoice created succesfully")
#         return redirect('invoices')

       
#     return render(request,"create_invoice.html",locals())


@login_required
def create_invoice(request):
    phone = request.session.get("phone")
    customers = Customer.objects.all()
    products = Product.objects.filter(stock__gt=0).order_by('name')
    customer = None
    total = 0

    # If phone in session, get the customer object
    if phone:
        customer = Customer.objects.filter(phone=phone).first()

    if request.method == "POST":
        # On form submit for invoice, check if customer exists
        if not customer:
            messages.error(request, "No customer selected. Please select a customer first.")
            return redirect('create_invoice')

        # Check if products selected
        selected_products = request.POST.getlist("products[]")
        if not selected_products:
            messages.error(request, "Did you forget to select the product?")
            return redirect('create_invoice')

        qtys = request.POST.getlist("qty[]")

        invoice = Invoice.objects.create(customer=customer, staff=request.user)
        
        for i in range(len(selected_products)):
            product = Product.objects.get(id=selected_products[i])
            requested_qty = int(qtys[i])

            # Check if requested quantity exceeds available stock
            if requested_qty > product.stock:
                messages.error(request, f"Requested quantity for {product.name} exceeds available stock ({product.stock}).")
                invoice.delete()  # Delete the partially created invoice
                return redirect('create_invoice')

            sub_total = product.price * Decimal(requested_qty)
            invoice_item = InvoiceItem.objects.create(
                invoice=invoice,
                product=product,
                quantity=requested_qty,
                sub_total=sub_total
            )
            product.stock -= requested_qty
            product.save()
            total += invoice_item.sub_total

        invoice.total = total
        tax = total * (Decimal(invoice.gst_percentage / 100))
        grand_total = total + tax
        invoice.grand_total = grand_total
        invoice.save()

        # Clear the session after invoice created
        del request.session['phone']
        messages.success(request, "Invoice created successfully")
        return redirect('invoices')

    # GET request: just render the invoice creation page
    return render(request, "create_invoice.html", locals())




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
def existing_customer(request):
    if request.method == "POST":
        phone=request.POST.get("phone")
        request.session['phone'] = phone
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
        'invoice':invoice,
        'invoice_item':invoice_item,
        'tax':tax
    }
    return render_to_pdf("invoice_pdf.html",context)