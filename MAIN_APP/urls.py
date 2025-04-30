from MAIN_APP import views
from django.urls import path 

urlpatterns = [
    path('',views.index, name='index'),
    path('login_page/',views.login_page, name='login_page'),
    path('logout_page/',views.logout_page, name='logout_page'),
    path('signup_page/',views.signup_page, name='signup_page'),
    path('dashboard/',views.dashboard, name='dashboard'),
]