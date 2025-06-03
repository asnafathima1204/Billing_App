from django.urls import path
from BILLING import views

urlpatterns = [
    path('',views.invoices,name="invoices"),
    path('create_invoice/',views.create_invoice,name="create_invoice"),
    path('new_customer/',views.new_customer,name="new_customer"),
    path('search_cutomer/',views.search_cutomer,name="search_cutomer"),
    path('view_invoice/<int:id>',views.view_invoice,name="view_invoice"),
    path('invoice_pdf/<int:id>',views.invoice_pdf,name="invoice_pdf"),
    path('edit_invoice/<int:id>',views.edit_invoice,name="edit_invoice"),

]
