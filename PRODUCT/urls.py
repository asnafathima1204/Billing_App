from django.urls import path
from PRODUCT import views

urlpatterns = [
    path('',views.products_list,name="products_list"),
    path('view/<int:id>/',views.product_view,name="product_view"),
    path('add_product/',views.add_product,name="add_product"),
]