from django.shortcuts import render,redirect,get_object_or_404
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
    cart=None
    cart_item=None
    # cart = request.session.get('cart',[])
    # product_ids = [item['product_id'] for item in cart]
    # cart_products=Product.objects.filter(id__in=product_ids)
    # If phone in session, get the customer object
    if phone:
        customer = Customer.objects.get(phone=phone)
        cart=Cart.objects.filter(customer=customer).first()
        if not cart:
            cart=Cart.objects.create(customer=customer)
    
    
    search=request.GET.get("search_product")
    if search:
        products=Product.objects.filter(Q(name__icontains=search) & Q(stock__gt=0))
        if not products.exists():
            messages.error(request, "Requested product not found!")
            return redirect('create_invoice')
            
    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add_product":
            # products=None
            product_id = request.POST.get("product_id")
            product=get_object_or_404(Product, id=product_id)
            if not cart:
                messages.error(request,"Have you forget to choose a customer")
                return redirect('create_invoice')
                
            
            cart_item=CartItem.objects.filter(cart=cart,product=product).first()
            if cart_item:
                product_stock = int(cart_item.product.stock)
                if cart_item.quantity < product_stock:
                    cart.total -= cart_item.sub_total

                    cart_item.quantity += 1
                    cart_item.sub_total = cart_item.product.price * cart_item.quantity
                    cart_item.save()

                    cart.total += cart_item.sub_total
                    gst=cart.total * Decimal((cart.gst_percentage/100))
                    cart.gst = gst
                    cart.grand_total = cart.total + cart.gst
                    cart.save()
                    return redirect('create_invoice')
                else:
                    cart.total -= cart_item.sub_total

                    cart_item.quantity = product_stock
                    cart_item.sub_total = cart_item.product.price * product_stock
                    cart_item.save()

                    cart.total += cart_item.sub_total
                    gst=cart.total * Decimal((cart.gst_percentage/100))
                    cart.gst = gst
                    cart.grand_total = cart.total + cart.gst
                    cart.save()

                    messages.warning(request, f"Only {product.stock} items available in stock.")
                    return render(request,'create_invoice',locals())
            else:
                cart_item=CartItem.objects.create(product=product,cart=cart)
                cart_item.sub_total = cart_item.product.price * cart_item.quantity
                cart_item.save()

                cart.total += cart_item.sub_total
                gst=cart.total * Decimal((cart.gst_percentage/100))
                cart.gst = gst
                print(cart.gst)
                cart.grand_total = cart.total + cart.gst
                cart.save()
            return redirect('create_invoice')
        
            
        elif action == "update_quantity":
            item_id=int(request.POST.get("item_id"))
            quantity=int(request.POST.get("quantity"))
            print("quantity:",quantity)
            cart_item=CartItem.objects.get(id=item_id)
            product_stock = int(cart_item.product.stock)
            if quantity <= product_stock and quantity >= 1:
                cart.total -= cart_item.sub_total

                cart_item.quantity = quantity
                cart_item.sub_total=cart_item.product.price * int(quantity)
                print(cart_item.sub_total)
                cart_item.save()

                cart.total += cart_item.sub_total
                gst=cart.total * Decimal((cart.gst_percentage/100))
                cart.gst = gst
                cart.grand_total = cart.total + cart.gst
                cart.save()
                return redirect('create_invoice')
            else:
                if quantity > product_stock:
                    messages.warning(request, f"Maximum available stock of {cart_item.product} is {product_stock}.")
                    cart.total -= cart_item.sub_total

                    cart_item.quantity = product_stock
                    cart_item.sub_total = cart_item.product.price * product_stock
                    cart_item.save()

                    cart.total += cart_item.sub_total
                    gst=cart.total * Decimal((cart.gst_percentage/100))
                    cart.gst = gst
                    cart.grand_total = cart.total + cart.gst
                    cart.save()
                    return redirect('create_invoice')
                elif quantity < 1:
                    messages.warning(request,f"Quantity for { cart_item.product } was less than 1. It has been reset to 1 automatically.")
                    cart.total -= cart_item.sub_total

                    cart_item.quantity = 1
                    cart_item.sub_total = cart_item.product.price * cart_item.quantity
                    cart_item.save()

                    cart.total += cart_item.sub_total
                    gst=cart.total * Decimal((cart.gst_percentage/100))
                    cart.gst = gst
                    cart.grand_total = cart.total + cart.gst
                    cart.save()
                    return redirect('create_invoice')

            return redirect('create_invoice')


        
        elif action == "remove_product":
            item_id = int(request.POST.get("product_id"))
            print(item_id)
            cart_item=CartItem.objects.get(id=item_id)

            cart.total -= cart_item.sub_total
            gst=cart.total * Decimal((cart.gst_percentage/100))
            cart.gst = gst
            cart.grand_total = cart.total + cart.gst
            cart_item.delete()
            cart.save()
            

            return redirect('create_invoice')  
        
        elif action == "save_invoice":
            if not phone:
                messages.error(request,"Did you forget to add a customer")
                return redirect('create_invoice')
            if not cart or not cart.cartitem_set.exists():
                messages.error(request,"Cart is empty, Add products before saving.")
                return redirect('create_invoice')
            
            invoice=Invoice.objects.create(
                customer = cart.customer,
                staff = request.user,
                date=datetime.now(),
                total = cart.total,
                grand_total = cart.grand_total,
                gst=cart.gst

            )

            for item in CartItem.objects.filter(cart=cart):
                invoice_item=InvoiceItem.objects.create(
                    invoice=invoice,
                    product=item.product,
                    quantity=item.quantity,
                    sub_total=item.sub_total
                )

                item.product.stock -= item.quantity
                item.product.save()
            
            CartItem.objects.filter(cart=cart).delete()
            cart.delete()

            messages.success(request,"Invoice created successfully!")
            return redirect('invoices')
            
    cart_items=CartItem.objects.filter(cart=cart)
    print(cart_items)
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


    context={
        'request': request,
        'invoice':invoice,
        'invoice_item':invoice_item
    }
    return render_to_pdf("invoice_pdf.html",context)


