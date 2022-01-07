from django.contrib import messages
from django.http.response import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import ListView
from datetime import date
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import *
from auser.models import *
from post.models import *
from .forms import *


class ShopAdmin(LoginRequiredMixin, View):
    raise_exception = True
    template_name = 'shop_admin.html'
    model = Shop
    model1 = MUser
    form = TagCreateForm()

    def get(self, request, id, **kwargs):
        if request.user.id == id:
            user = self.model1.objects.get(id=id)
            form = TagCreateForm()
            try:
                shop = self.model.objects.get(owner=user)
                return render(request, 'shop_admin.html', {'user': user, 'shop': shop, 'form': form})
            except:
                return render(request, 'shop_admin.html', {'user': user})
        else:
            raise Http404('شما اجازه ورود به این صفحه را ندارید')

    def post(self, request, *args, **kwargs):
        form = TagCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'تگ جدید اضافه شد')
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


class ShopRegister(LoginRequiredMixin, View):
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
            messages.info(request, 'درخواست ثبت فروشگاه ارسال شد')
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[id]))


class AddProduct(LoginRequiredMixin, View):
    model = Shop

    def get(self, request, id, **kwargs):
        if request.user.id == id:
            if self.model.objects.get(owner=request.user).status == 'confirmed' and self.model.objects.get(owner=request.user).delete_status == 'undelete':
                form = NewProduct()
                return render(request, 'add_product.html', {'form': form})
            else:
                messages.error(request, 'وضعیت فروشگاه شما تایید شده نیست')
                return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))
        else:
            raise Http404('شما اجازه ورود به این صفحه را ندارید')

    def post(self, request, id):
        if self.model.objects.get(owner=request.user).status == 'confirmed' and self.model.objects.get(owner=request.user).delete_status == 'undelete':
            form = NewProduct(request.POST, request.FILES)
            if form.is_valid():
                new_product = form.save(commit=False)
                new_product.shop = self.model.objects.get(owner=request.user)
                new_product.save()
                new_product = form.save_m2m()
                messages.info(request, 'محصول ثبت شد')
                return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


class ShopBasketView(LoginRequiredMixin, View):

    model = ListOfComodity
    model1 = ShopBasket
    model2 = Order
    model3 = Shop
    form = ShopBasketForm()
    search_form = ShopBasketSearchForm()

    def get(self, request, id, **kwargs):
        if request.user.id == id:
            if self.model3.objects.get(owner=request.user).delete_status == 'undelete':
                shop_basket = self.model1.objects.filter(
                    shop=self.model3.objects.get(owner=request.user)).order_by('created_on')
                form = ShopBasketForm()
                search_form = ShopBasketSearchForm()
                return render(request, 'shop_basket.html', {'shop_basket': shop_basket, 'form': form, 'search_form': search_form, id: {request.user.id}})
            else:
                messages.error(request, 'وضعیت فروشگاه شما تایید شده نیست')
                return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))
        else:
            raise Http404('شما اجازه ورود به این صفحه را ندارید')

    def post(self, request, id, **kwargs):
        if self.model3.objects.get(owner=request.user).delete_status == 'undelete':
            search_form = ShopBasketSearchForm(request.POST or None)
            form = ShopBasketForm(request.POST or None)
            if search_form.is_valid():
                begin_date = search_form.cleaned_data['begin_date']
                end_date = search_form.cleaned_data['end_date']
                if search_form.cleaned_data['status'] != 'all':
                    shop_basket = self.model1.objects.filter(
                        status=search_form.cleaned_data['status'], shop=self.model3.objects.get(owner=request.user), created_on__gte=begin_date, created_on__lte=end_date).order_by('created_on')
                    form = ShopBasketForm()
                    search_form = ShopBasketSearchForm()
                    return render(request, 'shop_basket.html', {'shop_basket': shop_basket, 'form': form, 'search_form': search_form, 'id': {request.user.id}})
                if search_form.cleaned_data['status'] == 'all':
                    shop_basket = self.model1.objects.filter(shop=self.model3.objects.get(
                        owner=request.user), created_on__gte=begin_date, created_on__lte=end_date).order_by('created_on')
                    form = ShopBasketForm()
                    search_form = ShopBasketSearchForm()
                    return render(request, 'shop_basket.html', {'shop_basket': shop_basket, 'search_form': search_form, 'form': form, id: {request.user.id}})
        else:
            messages.error(request, 'شما فروشگاه خود را حذف کردید')
            return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


class ShopBasketDetailView(LoginRequiredMixin, View):
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
        form = ShopBasketForm(request.POST or None, instance=shop_basket)
        if form.is_valid():
            form.save()
            return redirect(reverse('sell:shop_basket', args=[request.user.id]))


class ShopEditView(LoginRequiredMixin, View):
    model = ListOfComodity
    model1 = ShopBasket
    model2 = Order
    model3 = Shop

    def get(self, request, id, **kwargs):
        if request.user.id == id:
            shop = self.model3.objects.get(owner=request.user)
            form = NewShop()
            return render(request, 'shop_edit.html', {'shop': shop, 'form': form, id: {request.user.id}})
        else:
            raise Http404('شما اجازه ورود به این صفحه را ندارید')

    def post(self, request, id, **kwargs):
        shop = self.model3.objects.get(owner=request.user)
        form = NewShop(request.POST or None, instance=shop)
        if form.is_valid():
            edited_shop = form.save(commit=False)
            edited_shop.status = 'processing'
            edited_shop.save()
            messages.info(request, 'درخواست تغییرات ارسال شد')
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
