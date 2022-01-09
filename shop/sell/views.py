from django.contrib import messages
from django.db.models.query import QuerySet
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
# rest
from django.contrib.auth.models import User, Group
from rest_framework import request, viewsets
from rest_framework import permissions
from .serializers import *
from django.http.response import Http404
from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.response import Response
from rest_framework import generics, mixins

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .filter import *


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


# rest

class UserRegister(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = MUser.objects.all()
    serializer_class = UserSerializer

# this get is just for convinient and should be omited

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response(status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer['username'].value)
        user = MUser.objects.create_user(
            serializer['username'].value, serializer['email'].value, serializer['password'].value, phonenumber=serializer['phonenumber'].value)
        resp_serializer = ProfileSerializer(user)
        headers = self.get_success_headers(serializer.data)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()


class ProfileRegister(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get(self, request):
        user_profile = Profile.objects.get(costumer=self.request.user)
        serializer = self.get_serializer(user_profile)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request):

        profile = Profile.objects.get(costumer=self.request.user)
        serialized = ProfileSerializer(profile, data=request.data)

        if serialized.is_valid():
            serialized.update(profile, serialized.validated_data)
            return Response(data={"status": "api_user_update_ok"}, status=status.HTTP_201_CREATED)

        else:
            return Response(data={"status": "api_user_update_failed", "error": serialized.errors.get('email')[0]}, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        profile = self.perform_create(serializer)
        resp_serializer = ProfileSerializer(profile)
        headers = self.get_success_headers(serializer.data)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save(costumer=self.request.user)


class ShopList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Shop.objects.filter(status='confirmed')
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer
    filterset_class = ShopTypeFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class TypeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TypeSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class ProductList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ListOfComodity.objects.filter(status='existing')
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    filterset_class = ShopTypeFilter

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class AddShopBasket(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ShopBasketSerializer
    QuerySet = ListOfComodity.objects.all()

    def post(self, request, *args, **kwargs):
        print(ShopBasket.objects.all())
        if not ShopBasket.objects.filter(costumer=self.request.user, status='processing'):
            self.shop = ListOfComodity.objects.get(
                id=kwargs['product_id']).shop
            return self.create(request, *args, **kwargs)
        else:
            shop_basket = ShopBasket.objects.get(
                costumer=self.request.user, status='processing')
            resp_serializer = ShopBasketSerializer(shop_basket)
            return Response(resp_serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        self.shop = ListOfComodity.objects.get(id=kwargs['product_id']).shop
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_basket = self.perform_create(serializer)
        resp_serializer = ShopBasketSerializer(shop_basket)
        # headers = self.get_success_headers(serializer.data)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save(costumer=self.request.user, shop=self.shop)


class AddOrder(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    QuerySet = Order.objects.all()

    def post(self, request, *args, **kwargs):
        print(kwargs['number'])
        # self.shop_basket = ShopBasket.objects.filter(
        #     costumer=self.request.user, status='processing')
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        self.shop_basket = ShopBasket.objects.filter(
            costumer=self.request.user, status='processing')[0]
        self.product = ListOfComodity.objects.get(id=kwargs['product_id'])
        self.number = kwargs['number']
        print(self.product.remaining_stock)
        print(self.number)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = self.perform_create(serializer)
        resp_serializer = OrderSerializer(order)
        # headers = self.get_success_headers(serializer.data)
        return Response(resp_serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        return serializer.save(costumer=self.request.user, shop_basket=self.shop_basket, number=self.number, comodity=self.product)


class DeleteOrder(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    lookup_field = 'id'
    lookup_url_kwarg = 'id'

    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    QuerySet = Order.objects.all()

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class DeleteOrder(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, id):
        try:
            return Order.objects.get(id=id)
        except Order.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet)
    #     return Response(serializer.data)

    # def put(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet, data=request.DATA)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        order = self.get_object(id)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PayShopBasket(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """

    def get_object(self, id):
        try:
            return ShopBasket.objects.get(id=id)
        except ShopBasket.DoesNotExist:
            raise Http404

    # def get(self, request, pk, format=None):
    #     snippet = self.get_object(pk)
    #     serializer = SnippetSerializer(snippet)
    #     return Response(serializer.data)

    def put(self, request, id, format=None):
        shop_basket = self.get_object(id)
        serializer = ShopBasketSerializer(shop_basket, data=request.data)
        if serializer.is_valid():
            serializer.save(status='payed')
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, id, format=None):
    #     order = self.get_object(id)
    #     order.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)


class ShopBasketCostumerList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # queryset = ShopBasket.objects.filter(costumer=request.user)
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopBasketSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return ShopBasket.objects.filter(
            costumer=self.request.user)


class OpenShopBasketCostumerList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    # queryset = ShopBasket.objects.filter(
    #     costumer=request.user, status='processing')
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopBasket

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        return ShopBasket.objects.filter(
            costumer=self.request.user, status='processing')
