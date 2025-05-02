from django.urls import path
from BILLING import views

urlpatterns = [
    path('',views.billing_list,name="billing_list")
]
