from django.shortcuts import render

from posts.models import Post

# Create your views here.
def posts_list(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'post_list.html', context)