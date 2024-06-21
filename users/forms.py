from cProfile import Profile

from django import forms
from .models import Message, CustomUser


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'email', 'bio', 'phone', 'profile_picture')