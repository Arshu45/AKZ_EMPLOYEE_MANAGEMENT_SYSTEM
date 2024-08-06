from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.SignupPage, name='signup'),
    path('login', views.LoginPage, name='login'),
    path('homepage', views.index, name='index'),
    path('all_emp', views.all_emp, name='all_emp'),
    path('add_emp/', views.add_emp, name='add_emp'),
    path('emp/<int:emp_id>/', views.view_emp, name='view_emp'),
    path('remove_emp', views.remove_emp, name='remove_emp'),
    path('remove_emp/<int:emp_id>', views.remove_emp, name='remove_emp'),
    path('filter_emp', views.filter_emp, name='filter_emp'),
    path('update/<int:emp_id>/', views.update_emp, name='update_emp'),
    path('logout', views.logout_view, name='logout'),
    # path('protected/', ProtectedView.as_view(), name='protected'),
    # path('update_emp/<int:emp_id>/', views.update_emp, name='update_emp'),
]
