from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Userregistration , Products
from django.contrib.auth.hashers import make_password,check_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import *
from django.core.files.storage import FileSystemStorage
# Create your views here.

def index(request):
    return HttpResponse("Home Page")


# def admin(request):
#     return render(request , 'users/admin.html')


def customer(request):
    pro = Products.objects.exclude(status='Inactive')
    return render(request, 'users/customer.html', { 'pr': pro})

# def admin(request):
#     if request.method == 'GET':
#         return render(request,'users/admin.html')
#     else:
#         name =request.POST.get('name')
#         price = request.POST.get('price')
#         quantity =request.POST.get('quantity')
#         status =request.POST.get('status')
#         image = request.POST.get('image')
#         products = Products(name=name, price=price, quantity=quantity, status=status, image=image)
#         products.reg()
#         return render(request, 'users/admin.html')
def admin(request):

    if request.method == 'POST':
        form = ProductsForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('admin')
    else:
        form = ProductsForm()
        pro = Products.objects.all()
    return render(request, 'users/admin.html', {'form': form , 'pr':pro})

def update_data(request,id):
    if request.method == 'POST':
        pi = Products.objects.get(pk=id)
        form = ProductsForm(request.POST,request.FILES,instance=pi)
        if form.is_valid():
            form.save()
    else:
        pi = Products.objects.get(pk=id)
        form = ProductsForm( instance=pi)

    return render(request, 'users/updateproduct.html',{'form':form})

def delete_data(request , id):
    if request.method == 'POST':
        pi = Products.objects.get(pk=id)
        pi.delete()
        return redirect('admin')



def register(request):
    if request.method == 'GET':
        return render(request,'users/register.html')
    else:
        postdata = request.POST
        email = postdata.get('email')
        password = postdata.get('password')
        role = postdata.get('role')
        customer = Userregistration(email=email, password=password, role=role)
        #validation
        value = {
            'email' : email,
            'role' : role
        }
        error_message= None
        if(not role):
            error_message = "Role required"

        elif customer.isExists():
            error_message= "Email Already Registered"
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return HttpResponse("Register Successful")
        else:
            data = {
                'error': error_message,
                'values' : value
            }
            return render(request, 'users/register.html',data)

def login(request):
    if request.method == "GET" :
        return render(request, 'users/login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Userregistration.get_customer_by_email(email)
        error_message = None
        if customer:
           flag = check_password(password,customer.password)
           if flag:
               if customer.role == "admin":
                    return redirect('admin')
               else:
                   return redirect('customer')
           else:
               error_message = "Email or password Invalid"
        else:
            error_message = "Email or password Invalid"
        print(email,password)
        return render(request, 'users/login.html', {'error': error_message})

def logout_page(request):
    logout(request)
    return redirect('login')