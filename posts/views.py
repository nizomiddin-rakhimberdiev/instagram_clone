from django.shortcuts import render, redirect

from posts.models import Post

# Create your views here.
def posts_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'post_list.html', context)
    else:
        return redirect('users:login')