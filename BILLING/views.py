from django.shortcuts import render
from BILLING.models import *

# Create your views here.
def invoices(request):
    invoices=Invoice.objects.all()
    return render(request,"invoices.html",locals())

def create_invoice(request):
    return render(request,"create_invoice.html")


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
