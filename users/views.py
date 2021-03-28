from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import Userregistration , Products , Cart
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
    if request.session.get('customer_id') == "customer":
        pro = Products.objects.exclude(status='Inactive')
        pro = Products.objects.exclude(quantity='0')
        return render(request, 'users/customer.html', { 'pr': pro})
    else:
        return redirect('login')





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
    if request.session.get('customer_id') == "admin" :

        if request.method == 'POST':
            form = ProductsForm(request.POST, request.FILES)

            if form.is_valid():
                form.save()
                return redirect('admin')
                
        else:
            form = ProductsForm()
            pro = Products.objects.exclude(quantity='0')
            
        return render(request, 'users/admin.html', {'form': form , 'pr':pro})
    else:
        return redirect('login')
def my_cart(request):
    if request.session.get('customer_id') == "customer" :
        if request.method == 'GET':
            email = request.session.get('customer_email')
            pro = Cart.objects.filter(email=email)
            # pro = Cart.objects.exclude(quantity='0')
            return render(request, 'users/cart.html',{ 'pr':pro })
    else:
        return redirect('login')


def add_to_cart(request,id):
    if request.method == 'GET':
        return redirect('customer')
    else:
            pi = Products.objects.get(pk=id)
            a  = request.session.get('customer_email')
            b = pi.name
            c = pi.price
            d = 1
            e =  pi.image
            email = a
            name = b
            price = c
            quantity = d
            total_quantity = c
            image =  e
            cart = Cart(email=email, name=name, price=price, quantity=quantity, image=image , total_quantity=total_quantity)
            pro = Cart.objects.all()
            if cart.incart():
                return redirect('customer')
            else:
                cart.re()
                pro_q = pi.quantity - 1
                Products.objects.filter(id=id).update(quantity=pro_q)
                return redirect('customer')

def add_quantity(request,id):
    if request.method == 'GET':
        return redirect('mycart')
    if request.method == 'POST':
        pi = Cart.objects.get(pk=id)
        name = pi.name
        pro = Products.objects.get(name=name)
        quantity = pi.quantity + 1
        total_quantity = quantity * pi.price
        pro_q = pro.quantity - 1
        Products.objects.filter(name=name).update(quantity=pro_q)
        Cart.objects.filter(id=id).update(quantity=quantity,total_quantity=total_quantity)
        return redirect('mycart')

def sub_quantity(request,id):
    if request.method == 'POST':
        pi = Cart.objects.get(pk=id)
        name = pi.name
        pro = Products.objects.get(name=name)
        quantity = pi.quantity - 1
        pro_q = pro.quantity + 1
        name = pi.name
        Products.objects.filter(name=name).update(quantity=pro_q)
        if quantity < 1:
            pi.delete()
        total_quantity = quantity * pi.price
        Cart.objects.filter(id=id).update(quantity=quantity,total_quantity=total_quantity)
        
        return redirect('mycart')

def update_data(request,id):
    if request.session.get('customer_id') == "admin":
        if request.method == 'POST':
            pi = Products.objects.get(pk=id)
            form = ProductsForm(request.POST,request.FILES,instance=pi)
            
            if form.is_valid():
                form.save()
        else:
            pi = Products.objects.get(pk=id)
            form = ProductsForm( instance=pi)
           

        return render(request, 'users/updateproduct.html',{'form':form})
    else:
        return redirect('login')

def delete_data(request , id):
    if request.method == 'POST':
        pi = Products.objects.get(pk=id)
        pi.delete()
        return redirect('admin')
def delete_cartdata(request , id):
    if request.method == 'POST':
        pi = Cart.objects.get(pk=id)
        name = pi.name
        pro = Products.objects.get(name=name)
        pro_q = pro.quantity + pi.quantity
        Products.objects.filter(name=name).update(quantity=pro_q)
        pi.delete()
        return redirect('mycart')



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
                    request.session['customer_id'] = customer.role
                    return redirect('admin')

               else:
                   request.session['customer_id'] = customer.role
                   request.session['customer_email'] = customer.email
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