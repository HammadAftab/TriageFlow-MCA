from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User


def login_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        dob = request.POST.get('dob')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            return render(request, 'login.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'login.html', {'error': 'Username already taken'})

        if User.objects.filter(email=email).exists():
            return render(request, 'login.html', {'error': 'Email already registered'})

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