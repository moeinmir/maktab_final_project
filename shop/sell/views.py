from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
from django.http import request
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.views.generic.base import TemplateView
from .models import *
from auser.models import *
from .forms import *
from django.views import View
from rest_framework import generics, mixins
from django.views.generic import TemplateView, ListView, DetailView


class ShopAdmin(View):
    template_name = 'shop_admin.html'
    model = Shop
    model1 = MUser

    def get(self, request, id, **kwargs):
        user = self.model1.objects.get(id=id)
        try:
            shop = self.model.objects.get(owner=user)
            return render(request, 'shop_admin.html', {'user': user, 'shop': shop})
        except:
            return render(request, 'shop_admin.html', {'user': user})


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
        form = NewProduct()
        return render(request, 'shop_register.html', {'form': form})

    def post(self, request, id):
        form = NewProduct(request.POST, request.FILES)
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.shop = self.model.objects.filter(owner=request.user)[0]
            new_product.save()
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


class ShopListView(ListView):
    model = ShopBasket
    paginate_by = 10


class ShopBasketDetailView(DetailView):
    model = ShopBasket
