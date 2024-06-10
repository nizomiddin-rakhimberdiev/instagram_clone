from django.shortcuts import render, redirect

from users.models import CustomUser

# Create your views here.

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password1')
        CustomUser.objects.create(username=username, email=email, password=password)
        return redirect('posts:post_list')
    
    return render(request, 'register.html')
