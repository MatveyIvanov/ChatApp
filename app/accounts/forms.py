from distutils.command.clean import clean
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.forms import ValidationError
from django.forms import ModelForm
from django.contrib.auth import password_validation, authenticate

from .models import ChatUser


class ChatUserCreationForm(UserCreationForm):

    class Meta:
        model = ChatUser
        fields = ('id', 'password1', 'password2')


class ChatUserChangeForm(UserChangeForm):

    class Meta:
        model = ChatUser
        fields = ('id', 'password')


class ChatUserAuthenticationForm(AuthenticationForm):

    class Meta:
        model = ChatUser
        fields = ('id', 'password')
