from django.urls import path
from BILLING import views

urlpatterns = [
    path('',views.invoices,name="invoices"),
    path('create_invoice/',views.create_invoice,name="create_invoice"),
    path('new_customer/',views.new_customer,name="new_customer"),
    path('search_customer',views.search_customer,name="search_customer"),
    path('add_product_to_cart/<int:id>',views.add_product_to_cart,name="add_product_to_cart"),
    path('search_product',views.search_product,name="search_product"),
    path('view_invoice/<int:id>',views.view_invoice,name="view_invoice"),
    path('invoice_pdf/<int:id>',views.invoice_pdf,name="invoice_pdf"),
    path('edit_wallet/<int:id>',views.edit_wallet,name="edit_wallet"),

]
