from django.urls import path
from BILLING import views

urlpatterns = [
    path('',views.invoices,name="invoices"),
    path('create_invoice/',views.create_invoice,name="create_invoice"),
    path('invoice_product/',views.invoice_product,name="invoice_product"),
    path('new_customer/',views.new_customer,name="new_customer"),
    path('existing_customer/',views.existing_customer,name="existing_customer"),
    path('view_invoice/<int:id>',views.view_invoice,name="view_invoice"),
]
