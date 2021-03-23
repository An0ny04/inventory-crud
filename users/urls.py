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
    path('<int:id>', views.update_data, name='update'),
]