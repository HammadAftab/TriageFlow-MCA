from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Employee


# =========================
# USER LOGIN
# =========================
def login_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user:
            login(request, user)
            return redirect('dashboard')

        return render(request, 'login.html', {
            'error': 'Invalid credentials'
        })

    return render(request, 'login.html')


# =========================
# USER SIGNUP
# =========================
def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match check
        if password != confirm_password:
            return render(request, 'login.html', {
                'error': 'Passwords do not match'
            })

        # Username uniqueness
        if User.objects.filter(username=username).exists():
            return render(request, 'login.html', {
                'error': 'Username already taken'
            })

        # Email uniqueness
        if User.objects.filter(email=email).exists():
            return render(request, 'login.html', {
                'error': 'Email already registered'
            })

        # Create user
        User.objects.create_user(
            username=username,
            password=password,
            full_name=full_name,
            email=email,
            dob=dob
        )

        return redirect('login')

    return render(request, 'login.html')



def logout_view(request):

    logout(request)
    return redirect('login')



def employee_login_view(request):

    if request.method == "POST":

        employee_id = request.POST.get('employee_id')
        password = request.POST.get('password')

        try:
            employee = Employee.objects.get(
                employee_id=employee_id
            )

            user = authenticate(
                request,
                username=employee.user.username,
                password=password
            )

            if user:
                login(request, user)
                return redirect('dashboard')

            return render(request, 'employee_login.html', {
                'error': 'Invalid credentials'
            })

        except Employee.DoesNotExist:

            return render(request, 'employee_login.html', {
                'error': 'Employee ID not found'
            })

    return render(request, 'employee_login.html')


def employee_signup_view(request):

    if request.method == "POST":

        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        position = request.POST.get('position')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Password match check
        if password != confirm_password:

            return render(request, 'employee_login.html', {
                'error': 'Passwords do not match'
            })

        # Email uniqueness
        if User.objects.filter(email=email).exists():

            return render(request, 'employee_login.html', {
                'error': 'Email already exists'
            })

        # Create Django user
        user = User.objects.create_user(
            username=email,
            password=password,
            full_name=full_name,
            email=email,
            dob=dob
        )

        # Create employee profile
        employee = Employee.objects.create(
            user=user,
            full_name=full_name,
            email=email,
            dob=dob,
            position=position
        )

        # Show generated employee ID
        return render(request, 'employee_success.html', {
            'employee_id': employee.employee_id
        })

    return render(request, 'employee_success.html', {
    'employee_id': employee.employee_id
})