from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout

from users.forms import MessageForm, EditProfileForm
from users.models import CustomUser, Message


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


def send_message_view(request, username):
    receiver = get_object_or_404(CustomUser, username=username)
    if request.method == 'POST':
        message = request.POST.get('content')
        sender = request.user
        Message.objects.create(content=message, sender=sender, receiver=receiver)

    sender_messages = Message.objects.filter(sender=request.user)
    receiver_messages = Message.objects.filter(receiver=request.user)

    combined_messages = sender_messages | receiver_messages
    combined_messages = combined_messages.order_by('timestamp')

    messages = Message.objects.filter(sender=request.user).order_by('-timestamp')
    friends = list()
    for message in messages:
        friends.append(message.receiver.username)
    friends = set(friends)

    return render(request, 'messages.html',
                  {'combined_messages': combined_messages, 'receiver': receiver, 'messages': messages,
                   'friends': friends})


@login_required
def inbox(request, username=None):
    users = CustomUser.objects.exclude(id=request.user.id)
    messages = None
    active_user = None
    form = None

    if username:
        active_user = get_object_or_404(CustomUser, username=username)
        messages = Message.objects.filter(
            sender=request.user, receiver=active_user
        ) | Message.objects.filter(
            sender=active_user, receiver=request.user
        )
        messages = messages.order_by('timestamp')
        form = MessageForm()

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = active_user
            message.save()
            return redirect('users:inbox', username=active_user.username)

    context = {
        'users': users,
        'messages': messages,
        'active_user': active_user,
        'form': form,
    }
    return render(request, 'inbox.html', context)


def edit_profile(request, username):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:profile_page', username=username)
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'edit_profile.html', {'form': form})
