from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
    path('admin', views.admin, name='admin'),
    path('customer', views.customer, name='customer'),
    path('logout', views.logout_page, name='logout'),
    path('delete/<int:id>/',views.delete_data,name='delete'),
    path('datadelete/<int:id>/',views.delete_cartdata,name='deletedata'),
    path('addquantity/<int:id>/',views.add_quantity,name='addquantity'),
    path('subquantity/<int:id>/',views.sub_quantity,name='subquantity'),
    path('cart/<int:id>/',views.add_to_cart,name='cart'),
    path('mycart', views.my_cart, name='mycart'),
    path('<int:id>', views.update_data, name='update'),
]