from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from users.models import CustomUser

# Create your views here.
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('posts:post_list')
    return render(request, 'login.html')
    
    return render(request, 'login.html')


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        user = CustomUser.objects.create(username=username, email=email, password=password)
        user.set_password(password)  # Yangi parolni hashlash va saqlash
        user.save()
        return redirect('posts:post_list')
    
    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('posts:post_list')