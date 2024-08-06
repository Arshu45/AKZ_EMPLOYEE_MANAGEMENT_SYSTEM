from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.db.models import ProtectedError
from .models import Employee, Department, Role
from datetime import datetime
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout


# Create your views here.

def index(request):
    return render(request, 'index.html')

#Thid will show us all the employees
def all_emp(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view_all_emp.html', context)

#this will add a new employee
def add_emp(request):
    if request.method == 'POST':
        try:
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            salary = int(request.POST['salary'])
            bonus = int(request.POST['bonus'])
            phone = int(request.POST['phone'])
            dept_id = int(request.POST['dept'])
            role_id = int(request.POST['role'])
            location = request.POST['location']
            hire_date = request.POST['hire_date']  
            
            # Check if department and role exist
            dept = Department.objects.get(id=dept_id)
            role = Role.objects.get(id=role_id)
            
            new_emp = Employee(
                first_name=first_name,
                last_name=last_name,
                salary=salary,
                bonus=bonus,
                phone=phone,
                dept=dept,
                role=role,
                location=location,
                hire_date=hire_date
            )
            new_emp.save()
            return redirect('all_emp')  # Redirect to all employees page
        except Department.DoesNotExist:
            return HttpResponse("Department does not exist")
        except Role.DoesNotExist:
            return HttpResponse("Role does not exist")
        except Exception as e:
            return HttpResponse(f"An Exception Occurred: {e}")
    elif request.method == 'GET':
        context = {
            'departments': Department.objects.all(),
            'roles': Role.objects.all()
        }
        return render(request, 'add_emp.html', context)
    else:
        return HttpResponse("An Exception Occurred! Employee has not been added")

#this will remove a particular employee
def remove_emp(request, emp_id=0):
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return redirect('all_emp')  # Redirect to all employees page after deletion
        except Employee.DoesNotExist:
            return HttpResponse("Please enter a valid Employee ID")
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'remove_emp.html', context)

#this will filter an employee
def filter_emp(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '')
        dept = request.POST.get('dept', '')
        role = request.POST.get('role', '')
        emps = Employee.objects.all()
        if first_name:
            emps = emps.filter(Q(first_name__icontains=first_name) | Q(last_name__icontains=first_name))
        if dept:
            emps = emps.filter(dept__name__icontains=dept)
        if role:
            emps = emps.filter(role__name__icontains=role)
        context = {
            'emps': emps
        }
        return render(request, 'view_all_emp.html', context)
    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception occurred')
 

def update_emp(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    
    if request.method == 'POST':
        try:
            emp.first_name = request.POST['first_name']
            emp.last_name = request.POST['last_name']
            emp.salary = int(request.POST['salary'])
            emp.bonus = int(request.POST['bonus'])
            emp.phone = int(request.POST['phone'])
            emp.location = request.POST['location']  # Add location field
            emp.hire_date = datetime.strptime(request.POST['hire_date'], '%Y-%m-%d').date()  # Add hire_date field
            
            dept_id = int(request.POST['dept'])
            role_id = int(request.POST['role'])
            
            # Check if department and role exist
            emp.dept = Department.objects.get(id=dept_id)
            emp.role = Role.objects.get(id=role_id)
            
            emp.save()
            return redirect('view_emp', emp_id=emp.id)  # Redirect to view employee details page
        except Department.DoesNotExist:
            return HttpResponse("Department does not exist")
        except Role.DoesNotExist:
            return HttpResponse("Role does not exist")
        except Exception as e:
            return HttpResponse(f"An Exception Occurred: {e}")
    else:
        context = {
            'emp': emp,
            'departments': Department.objects.all(),
            'roles': Role.objects.all()
        }
        return render(request, 'update_emp.html', context)
#for registering an employee
def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Passwords do not match")
        else:
            # Check if username or email already exists
            if User.objects.filter(username=username).exists():
                return HttpResponse("Username already exists")
            elif User.objects.filter(email=email).exists():
                return HttpResponse("Email already exists")
            else:
                my_user = User.objects.create_user(username=username, email=email, password=pass1)
                my_user.first_name = fname
                my_user.last_name = lname
                my_user.save()
                return redirect('login')

    return render(request, 'signup.html')

#for Login an employee
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(username, password)

        if user is not None:
            login(request, user)
            return redirect('index')  # Redirect to the home page or another page after successful login
        else:
            return HttpResponse("Invalid username or password")

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('signup')  # Redirect to home page after logout


def update_emp(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    
    if request.method == 'POST':
        try:
            # Check if any of the restricted fields are being updated
            if (
                'first_name' in request.POST or
                'last_name' in request.POST or
                'hire_date' in request.POST
            ):
                return HttpResponseBadRequest("First name, last name, and hire date cannot be updated.")
            
            # Update other fields
            emp.salary = int(request.POST['salary'])
            emp.bonus = int(request.POST['bonus'])
            emp.phone = int(request.POST['phone'])
            emp.location = request.POST['location']
            
            dept_id = int(request.POST['dept'])
            role_id = int(request.POST['role'])
            
            # Check if department and role exist
            emp.dept = Department.objects.get(id=dept_id)
            emp.role = Role.objects.get(id=role_id)
            
            emp.save()
            return redirect('all_emp')  # Redirect to the 'all_emp' view after successful update
        except Department.DoesNotExist:
            return HttpResponse("Department does not exist")
        except Role.DoesNotExist:
            return HttpResponse("Role does not exist")
        except Exception as e:
            return HttpResponse(f"An Exception Occurred: {e}")
    else:
        context = {
            'emp': emp,
            'departments': Department.objects.all(),
            'roles': Role.objects.all()
        }
        return render(request, 'update_emp.html', context)

    
def view_emp(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    context = {
        'emp': emp
    }
    return render(request, 'view_emp.html', context)