from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
 
# Create your views here.
@login_required
def staff(request):
    users = User.objects.exclude(is_superuser=True)
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