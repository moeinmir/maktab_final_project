from django import views
from django.contrib.auth.models import User
from django.db.models.fields import DateField
from django.db.models.query import QuerySet
import psycopg2
from django.contrib import messages
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView

import shop
from .models import *
from auser.models import *
from post.models import *
from .forms import *
from django.views import View
from rest_framework import generics, mixins
from django.views.generic import TemplateView, ListView, DetailView
from datetime import date


class ShopAdmin(View):
    template_name = 'shop_admin.html'
    model = Shop
    model1 = MUser
    form = TagCreateForm()

    def get(self, request, id, **kwargs):
        user = self.model1.objects.get(id=id)
        form = TagCreateForm()
        try:
            shop = self.model.objects.get(owner=user)
            return render(request, 'shop_admin.html', {'user': user, 'shop': shop, 'form': form})
        except:
            return render(request, 'shop_admin.html', {'user': user})

    def post(self, request, *args, **kwargs):
        form = TagCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


class ShopRegister(View):
    model1 = MUser

    def get(self, request, id, **kwargs):
        form = NewShop()
        user = self.model1.objects.get(id=id)
        return render(request, 'shop_register.html', {'form': form, 'user': user})

    def post(self, request, id):
        form = NewShop(request.POST)
        if form.is_valid():
            new_shop = form.save(commit=False)
            new_shop.owner = request.user
            new_shop.save()
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[id]))


class AddProduct(View):
    model = Shop

    def get(self, request, id, **kwargs):
        if self.model.objects.get(owner=request.user).status == 'confirmed' and self.model.objects.get(owner=request.user).delete_status == 'undelete':
            form = NewProduct()
            return render(request, 'add_product.html', {'form': form})
        else:
            messages.error(request, 'your status is not confirmed')
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))

    def post(self, request, id):
        if self.model.objects.get(owner=request.user).status == 'confirmed' and self.model.objects.get(owner=request.user).delete_status == 'undelete':
            form = NewProduct(request.POST, request.FILES)
            if form.is_valid():
                new_product = form.save(commit=False)
                new_product.shop = self.model.objects.get(owner=request.user)
                new_product.save()
                return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


class ShopBasketView(View):

    model = ListOfComodity
    model1 = ShopBasket
    model2 = Order
    model3 = Shop

    def get(self, request, id, **kwargs):
        if self.model3.objects.get(owner=request.user).delete_status == 'undelete':
            search_form = ShopBasketForm()
            shop_basket = self.model1.objects.filter(
                shop=self.model3.objects.get(owner=request.user)).order_by('created_on')
            form = ShopBasketForm()
            search_form = ShopBasketSearchForm()
            return render(request, 'shop_basket.html', {'shop_basket': shop_basket, 'form': form, 'search_form': search_form, id: {request.user.id}})
        else:
            messages.error(request, 'your status is deleted')
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))

    def post(self, request, id, **kwargs):
        if self.model3.objects.get(owner=request.user).delete_status == 'undelete':
            search_form = ShopBasketSearchForm(request.POST or None)
            if search_form.is_valid():
                begin_date = search_form.cleaned_data['begin_date']
                if begin_date == None:
                    begin_date = date(2015, 5, 18)
                end_date = search_form.cleaned_data['end_date']
                if end_date == None:
                    end_date = date(2500, 5, 18)
                if search_form.cleaned_data['status'] != 'all':
                    shop_basket = self.model1.objects.filter(
                        status=search_form.cleaned_data['status'], shop=self.model3.objects.get(owner=request.user), created_on__gte=begin_date, created_on__lte=end_date).order_by('created_on')
                    return render(request, 'shop_basket.html', {'shop_basket': shop_basket, 'search_form': search_form, id: {request.user.id}})
                else:
                    shop_basket = self.model1.objects.filter(shop=self.model3.objects.get(
                        owner=request.user), created_on__gte=begin_date, created_on__lte=end_date).order_by('created_on')
                return render(request, 'shop_basket.html', {'shop_basket': shop_basket, 'search_form': search_form, id: {request.user.id}})
        else:
            messages.error(request, 'your status is deleted')
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


class ShopBasketDetailView(View):
    model = ListOfComodity
    model1 = ShopBasket
    model2 = Order
    model3 = Shop

    def get(self, request, id, **kwargs):
        shop_basket = self.model1.objects.get(id=id)
        order = self.model2.objects.filter(shop_basket=id)
        return render(request, 'shop_basket_details.html', {'order': order, 'shop_basket': shop_basket})

    def post(self, request, id, **kwargs):
        shop_basket = self.model1.objects.get(id=id)
        print(shop_basket.status)
        form = ShopBasketForm(request.POST or None, instance=shop_basket)
        if form.is_valid():
            form.save()
            return redirect(reverse('sell:shop_basket', args=[request.user.id]))


class ShopEditView(View):
    model = ListOfComodity
    model1 = ShopBasket
    model2 = Order
    model3 = Shop

    def get(self, request, id, **kwargs):
        shop = self.model3.objects.get(owner=request.user)
        form = NewShop()
        return render(request, 'shop_edit.html', {'shop': shop, 'form': form, id: {request.user.id}})

    def post(self, request, id, **kwargs):
        shop = self.model3.objects.get(owner=request.user)
        form = NewShop(request.POST or None, instance=shop)
        print('sdddddddddd')
        if form.is_valid():
            edited_shop = form.save(commit=False)
            edited_shop.status = 'processing'
            edited_shop.save()
            return redirect(reverse('sell:shop_admin', args=[request.user.id]))


class ComodityListView(ListView):
    model = ListOfComodity
    model1 = MUser
    model2 = Shop
    context_object_name = 'comodity_list'
    template_name = 'comodity_list_view.html'

    def get_queryset(self):
        return ListOfComodity.objects.filter(
            shop=self.model2.objects.get(owner=self.request.user))
