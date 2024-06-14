from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from posts.forms import PostForm
from posts.models import Post, Comment


# Create your views here.
def posts_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        context = {'posts': posts}
        return render(request, 'post_list.html', context)
    else:
        return redirect('users:login')


def create_post(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('posts:posts_list')

        else:
            form = PostForm()
        return render(request, 'create_post.html', {"form": form})


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        comment = request.POST['comment']
        Comment.objects.create(author=request.user, post=post, content=comment)
        return redirect('posts:add_comment', post_id=post_id)
    else:
        comments = Comment.objects.all().filter(post=post)
    return render(request, 'add_comment.html', {'post': post, 'comments': comments})