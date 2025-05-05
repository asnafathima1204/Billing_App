from django.urls import path
from BILLING import views

urlpatterns = [
    path('',views.invoice_list,name="invoice_list"),
    path('view_invoice/<int:id>',views.view_invoice,name="view_invoice"),
]
