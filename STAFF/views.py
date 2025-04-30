from django.shortcuts import render,redirect
from django.contrib.auth.models import User
 
# Create your views here.
def staff(request):
    users = User.objects.exclude(is_superuser=True)
    return render(request,"staff.html",locals())

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