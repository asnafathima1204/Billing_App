from STAFF import views
from django.urls import path 

urlpatterns = [
    path('',views.staff, name='staff'),
    path('activate_staff/<int:id>/',views.activate_staff, name='activate_staff'),
]