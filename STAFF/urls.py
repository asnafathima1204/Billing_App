from STAFF import views
from django.urls import path 

urlpatterns = [
    path('',views.staff, name='staff'),
    path('activate_staff/<int:id>/',views.activate_staff, name='activate_staff'),
    path('add_staff/',views.add_staff, name='add_staff'),
    path('update_staff/<int:id>/',views.update_staff, name='update_staff'),
    path('delete_staff/<int:id>/',views.delete_staff, name='delete_staff'),
    path('view_staff/<int:id>/',views.view_staff, name='view_staff'),
]