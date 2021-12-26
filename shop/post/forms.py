from django import forms
from django.forms import fields
from django.forms.fields import CharField
from .models import *
from django.contrib.auth.models import User

from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.db import models


# class RegisterForm(forms.Form):
#     class Meta:
#         model = User
#         fields = '__all__'


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['creator']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        exclude = '__all__'


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = '__all__'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
