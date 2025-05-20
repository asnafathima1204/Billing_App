from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required,user_passes_test
 
# Create your views here.
@user_passes_test(lambda u:u.is_authenticated and u.is_superuser,login_url='login_page' )
def staff(request):
    users = User.objects.exclude(is_superuser=True).order_by('-id')
    return render(request,"staff.html",locals())

@login_required
def activate_staff(request,id):
    user = User.objects.get(id=id)
    if user.is_staff:
        user.is_staff = False
        user.save()
        return redirect('staff')
    else:
        user.is_staff = True
        user.save()
    return redirect('staff')