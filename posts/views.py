from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
import random
from posts.forms import PostForm
from posts.models import Post, Comment
from users.models import CustomUser


# Create your views here.
def posts_list(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at')
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
                return redirect('posts:post_list')

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


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # liked = bool()
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    # return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})
    return redirect('posts:post_list')


def profile_page(request, username):
    # user = CustomUser.objects.get(username=username)
    posts = Post.objects.all().filter(author=request.user)
    len_posts = len(posts)
    context = {'posts': posts, 'len_posts': len_posts}
    return render(request, 'profile.html', context)


def explore_posts(request):
    posts = list(Post.objects.all())
    random.shuffle(posts)
    context = {'posts': posts}
    return render(request, 'explore.html', context)


def reels_list(request):
    posts = list(Post.objects.all())
    random.shuffle(posts)
    context = {'posts': posts}
    return render(request, 'reels.html', context)
