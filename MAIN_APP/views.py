from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def index(request):
    return render(request,'index.html')



def login_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username=email,password=password)
        if user is not None:
            if user.is_staff == 1:
                #admin/staff module
                login(request,user)
                return redirect('dashboard')
            else:
                messages.warning(request,"You are not authorized as staff yet. Please wait for admin approval.")
        else:
            if not User.objects.filter(username=email).exists():
                messages.warning(request,"You are not registered yetr. Please register..!")
                return redirect('signup_page')
            else:
                messages.error(request,"Wrong password")
                return redirect('login_page')
    # else:
    #     messages.error(request,"Invalid credentials")
    #     return redirect('login_page')
               
    return render(request,'login_page.html')

def logout_page(request):
    logout(request)
    return redirect('index')

def signup_page(request):
    if request.method == "POST":
        email = request.POST.get("email")
        f_name = request.POST.get("f_name")
        l_name = request.POST.get("l_name")
        password = request.POST.get("password")

        try:
            User.objects.get(username = email)
            messages.warning(request,"Email already exist. Please login...!!")
            return redirect('login_page')
        
        except User.DoesNotExist:
            user = User.objects.create(
                        username=email,
                        email=email,
                        first_name=f_name,
                        last_name=l_name,
                        password=password,
                    )
            user.set_password(password)
            user.save()
            messages.success(request,"Account created succesfully. Please login with your credentials")
            return redirect('login_page')

    return render(request,'signup_page.html')

@login_required
def dashboard(request):
    return render(request,'dashboard.html')
