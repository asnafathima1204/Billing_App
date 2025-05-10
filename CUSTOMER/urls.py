from django.urls import path
from CUSTOMER import views

urlpatterns = [
    path('',views.customers,name="customers"),
]
