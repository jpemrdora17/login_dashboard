from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Register Page
def registerPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            messages.success(request, "Account created successfully")
            return redirect('login')

    return render(request, 'accounts/register.html')

# Login Page
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, "Username OR Password is incorrect")

    return render(request, 'accounts/login.html')

# Logout
def logoutUser(request):
    logout(request)
    return redirect('login')

# Dashboard (Protected)
@login_required(login_url='login')
def dashboard(request):
    user = request.user 
    total_students = User.objects.count()

    context = {
        'user' : user,
        'total_students': total_students,
    }
    return render(request, 'accounts/dashboard.html', context)
