from django.contrib.messages.api import error
from django.db.models.fields import SlugField
from django.db.models import Q
from django.db.models.query import QuerySet
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import redirect, render, get_object_or_404
from .models import *
from .forms import *
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required


# from django.shortcuts import render,redirect,get_object_or_404
# from django.http import HttpResponse,HttpResponseNotFound
# from django.urls import reverse
from datetime import datetime


# Create your views here.


def post_list(request):
    posts = Post.objects.filter(status='Published')
    categories = Category.objects.all()
    return render(request, 'post.html', {'posts': posts, 'categories': categories})


def post_details(request, slug):
    form = CommentForm(request.POST or None)
    post = Post.objects.get(slug=slug)
    comment = Comment.objects.filter(related_post=post.id)
    if request.method == 'POST':
        if form.is_valid():
            form.save(commit=False)
            form.related_post = post
            form.save()

            return redirect(str('http://127.0.0.1:8000/blog/post_details/'+str(slug)))

    if request.method == 'GET':
        return render(request, 'post_details.html', {'post': post, 'comment': comment, 'form': form})


def category_details_view(request, category_id):

    category = Category.objects.get(id=category_id)

    posts = Post.objects.filter(post_category=category.id)
    print(posts)
    return render(request, 'category_details_view.html', {'posts': posts, 'category': category})


class CategoryListView(ListView):
    model = Category


def register_form(request):
    # form = RegisterForm(None or request.POST)
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = MUser.objects.create_user(
                form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password'])
            user.phonenumber = form.cleaned_data['phonenumber']
            user.user_type = form.cleaned_data['user_type']
            print(user)
            print(user.phonenumber)
            user.save()

            # messages.add_message(request, level=error,
            #                      message='A serious error occurred.')
        return render(request, 'register.html', {'form': form})

    if request.method == 'GET':
        return render(request, 'register.html', {'form': form})


def post_form(request):
    if request.method == 'POST':

        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            if request.user.user_type == 'Shop':

                n = form.save()
                print(n.creator)
                print(request.user)
                n.creator = request.user
                n.save()
                return redirect(reverse('post:post_list'))
            else:
                return redirect(reverse('post:post_list'))

    else:
        form = PostForm()
        return render(request, 'post_form.html', {'form': form})


# def comment_form(request):
#     form = CommentForm(request.POST or None)
#     if form.is_valid():
#         form.save()

#         return redirect(reverse('post:post_list'))

#     if request.method == 'GET':
#         return render(request, 'comment_form.html', {'form': form})


def category_form_edit(request, id):
    category = Category.objects.get(id=id)
    print(category)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect(reverse('post:post_list'))

    return render(request, 'category_form_edit.html', {
        'form': form
    })


def category_delete(request, id):
    print('fffffffffffffff')
    category = Category.objects.get(id=id)
    category.delete()
    return redirect(reverse('post:post_list'))


@ login_required(login_url='/login')
# @permission_required()
def post_form_edit(request, id):
    post = Post.objects.get(id=id)
    if request.user == post.creator:
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('post:post_list'))

        return render(request, 'post_form_edit.html', {
            'form': form
        })
    else:
        return redirect(reverse('post:post_list'))


def mylogin(request):
    form = LoginForm()
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            print(form.cleaned_data['username'])
            print(form.cleaned_data['password'])

            print(user)
            if user is not None:
                login(request, user)
                return redirect(reverse('post:post_form'))
            else:
                print('not found user')
    return render(request, 'login.html', {'form': form})


def search(request):
    q = request.GET.get('Q')

    if not q:
        Error_MSG = "Please enter the search keyword"
        messages.add_message(request, messages.ERROR,
                             Error_MSG, extra_tags='danger')
        return redirect(reverse('post:post_list'))

    post_list = Post.objects.filter(
        post_title__icontains=q) | Post.objects.filter(
        post_summery__icontains=q) | Post.objects.filter(
        post_content__icontains=q)
    categories = Category.objects.all()
    return render(request, 'post.html', {'posts': post_list, 'categories': categories})
