from drf_spectacular.utils import extend_schema
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from lib2to3.pgen2.token import NAME
from random import randint
from turtle import title
import redis
from drf_yasg.utils import swagger_auto_schema
from os import stat
import psycopg2
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
from django.db.models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .filter import *
from .melli.melli.melipayamak import Api
from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
import sys
sys.path.append("..")


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


class SellReport(LoginRequiredMixin, View):

    model = ListOfComodity
    model1 = ShopBasket
    model2 = Order
    model3 = Shop

    def get(self, request, id, **kwargs):

        user = ShopBasket.objects.filter(
            status='payed', shop=self.model3.objects.get(owner=self.request.user)).values(
            'costumer', 'costumer__username').annotate(total_buy=Sum('total_price')).annotate(number_of_buy=Count('costumer')).order_by('-total_buy')

        number_of_product = ShopBasket.objects.filter(
            status='payed', shop=self.model3.objects.get(owner=self.request.user)).values(
            'costumer', 'costumer__username').annotate(last_update=F('update_on'), number_of_product=Sum('order__number')).order_by('-number_of_product')

        total_sell = ShopBasket.objects.filter(
            status='payed', shop=self.model3.objects.get(owner=self.request.user)).aggregate(total_sell=Sum('total_price'))
        if request.user.id == id:
            if self.model3.objects.get(owner=request.user).delete_status == 'undelete':
                shop_basket = self.model1.objects.filter(
                    shop=self.model3.objects.get(owner=request.user)).order_by('created_on')

                return render(request, 'sell_report.html', {'shop_basket': shop_basket, 'user': user, 'total_sell': total_sell, 'number_of_product': number_of_product})
            else:
                messages.error(request, 'وضعیت فروشگاه شما تایید شده نیست')
                return HttpResponseRedirect(reverse('sell:shop_admin', args=[request.user.id]))


def chart(request):
    return render(request, 'sell_chart.html')


def sell_chart(request):
    labels = []
    data = []

    queryset = ShopBasket.objects.filter(status='payed', shop=Shop.objects.get(owner=request.user)).values('update_on').annotate(
        sell=Sum('total_price')).order_by('-update_on')
    for entry in queryset:
        labels.append(entry['update_on'])
        data.append(entry['sell'])

    return JsonResponse(data={
        'labels': labels,
        'data': data,
    })
# rest


class UserRegister(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = MUser.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_description="this part is for convinent and should be ommited in the operation", operation_summary="reciving users information")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="you can send your information through and if they are valid you will be registered as u user", operation_summary="user registering")
    def post(self, request, *args, **kwargs):
        self.create(request, *args, **kwargs)
        return Response(status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = MUser.objects.create_user(
                serializer['username'].value, serializer['email'].value, serializer['password'].value, phonenumber=serializer['phonenumber'].value)
            resp_serializer = UserSerializer(user)
            headers = self.get_success_headers(serializer.data)
            return Response(resp_serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(status=400)

    def perform_create(self, serializer):
        return serializer.save()


class ProfileRegister(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    @swagger_auto_schema(operation_description="if you are logged in and you have a profile you can recive its information through this link", operation_summary="recieving your profile information")
    def get(self, request):
        try:
            user_profile = Profile.objects.get(costumer=self.request.user)
            serializer = self.get_serializer(user_profile)
            return Response(serializer.data)
        except:
            return Response(status=400)

    @swagger_auto_schema(operation_description="if you are logged in you can send the data for your profile and if the data was valid your profile will be registered", operation_summary="registering the profile")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="if you are logged in and you have a profile you can modify its information through this link", operation_summary="modifying the profile")
    def put(self, request):

        profile = Profile.objects.get(costumer=self.request.user)
        serialized = ProfileSerializer(profile, data=request.data)

        if serialized.is_valid():
            serialized.update(profile, serialized.validated_data)
            return Response(data={"status": "api_user_update_ok"}, status=200)

        else:
            return Response(data={"status": "api_user_update_failed"}, status=400)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            profile = self.perform_create(serializer)
            resp_serializer = ProfileSerializer(profile)
            headers = self.get_success_headers(serializer.data)
            return Response(resp_serializer.data, status=200, headers=headers)
        else:
            return Response(status=400)

    def perform_create(self, serializer):
        return serializer.save(costumer=self.request.user)


class ShopList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Shop.objects.filter(status='confirmed')
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopSerializer
    filterset_class = ShopTypeFilter

    @swagger_auto_schema(operation_description="if you are logged in you can access to the information of confirmed shop through this link you can flter based on category too", operation_summary="recieving the list of confirmed shops")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class TypeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Category.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = TypeSerializer

    @swagger_auto_schema(operation_description="if you are logged in you can recive the list of shops category through this link", operation_summary="recieving shops categories")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)


class ProductList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = ListOfComodity.objects.filter(status='existing')
    permission_classes = (IsAuthenticated,)
    serializer_class = ProductSerializer
    filterset_class = ProductTypeFilter

    @swagger_auto_schema(operation_description="if you are logged in you can put the shop id in url and see its product and filter them based on tag and price", operation_summary="seeing the products of a shop")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        try:
            shop = Shop.objects.get(id=kwargs['shop_id'])
            queryset = self.filter_queryset(self.get_queryset())
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=200)
        except:
            return Response(status=400)

    def get_queryset(self):
        return self.queryset.filter(shop_id=self.kwargs.get('shop_id'))


class AddShopBasket(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = ShopBasketSerializer
    QuerySet = ListOfComodity.objects.all()

    @swagger_auto_schema(operation_description="if you are logged in you can put the id of a product in url and a cart in the shop related to that product will be created for you", operation_summary="registering a cart")
    def post(self, request, *args, **kwargs):
        try:
            self.shop = ListOfComodity.objects.get(
                id=kwargs['product_id']).shop

            if not ShopBasket.objects.filter(costumer=self.request.user, status='processing', shop=self.shop):
                # self.shop = ListOfComodity.objects.get(
                #     id=kwargs['product_id']).shop
                return self.create(request, *args, **kwargs)
            else:
                shop_basket = ShopBasket.objects.get(
                    costumer=self.request.user, status='processing', shop=self.shop)
                resp_serializer = ShopBasketSerializer(shop_basket)
                return Response({'message': 'you already had open shop basket', 'date': resp_serializer.data}, status=200)
        except:
            return Response(status=400)

    def create(self, request, *args, **kwargs):
        self.shop = ListOfComodity.objects.get(id=kwargs['product_id']).shop
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        shop_basket = self.perform_create(serializer)
        resp_serializer = ShopBasketSerializer(shop_basket)
        return Response({'message': 'a shop basket created', 'date': resp_serializer.data}, status=200)

    def perform_create(self, serializer):
        return serializer.save(costumer=self.request.user, shop=self.shop)


class AddOrder(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    QuerySet = Order.objects.all()

    @swagger_auto_schema(operation_description="if you are logged in you can register your order here if you dont have an open cart you should first make one", operation_summary="adding order")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        try:
            self.shop_basket = ShopBasket.objects.filter(
                costumer=self.request.user, status='processing')[0]
            self.product = ListOfComodity.objects.get(
                id=int(kwargs['product_id']))
            self.number = int(kwargs['number'])
            if int(self.number) <= self.product.remaining_stock:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                order = self.perform_create(serializer)
                resp_serializer = OrderSerializer(order)
                return Response(resp_serializer.data, status=200)
            else:
                return Response(status=400)
        except:
            return Response(status=400)

    def perform_create(self, serializer):
        return serializer.save(costumer=self.request.user, shop_basket=self.shop_basket, number=self.number, comodity=self.product)


class DeleteOrder(APIView):
    permission_classes = (IsAuthenticated,)

    def get_object(self, id):
        try:
            if self.request.user == Order.objects.get(id=id).costumer:
                return Order.objects.get(id=id)

        except Order.DoesNotExist:
            raise Http404

    @swagger_auto_schema(operation_description="if you are logged in you can put the id of the order you want to delete in url and sent the request", operation_summary="deleting order")
    def delete(self, request, id, format=None):
        order = self.get_object(id)
        self.product = order.comodity
        self.product.remaining_stock += order.number
        self.product.status = 'existing'
        self.product.save()
        self.shop_basket = order.shop_basket
        self.shop_basket.total_price -= order.number*self.product.price
        if self.shop_basket.total_price == 0:
            self.shop_basket.status = 'canceled'
        self.shop_basket.save()
        order.delete()
        return Response(status=200)


class PayShopBasket(APIView):

    def get_object(self, id):
        try:
            return ShopBasket.objects.get(id=id)
        except ShopBasket.DoesNotExist:
            raise Http404

    @swagger_auto_schema(request_body=ShopBasketSerializer, operation_description="you should put the cart id in the url and send the put request so cart be payed", operation_summary="paying the cart")
    # @extend_schema(description='text')
    def put(self, request, id, format=None):
        shop_basket = self.get_object(id)
        serializer = ShopBasketSerializer(shop_basket, data=request.data)
        if serializer.is_valid():
            serializer.save(status='payed')
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)


class ShopBasketCostumerList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ShopBasketSerializer

    @swagger_auto_schema(operation_description="if you are logged in you can send the get request and recieve your former carts information", operation_summary="list of former carts")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=200)

    def get_queryset(self):
        return ShopBasket.objects.filter(
            costumer=self.request.user, status='payed')


redis = redis.Redis(host='localhost', port='6379',
                    charset="utf-8", decode_responses=True)


class UserRegisterWithPhone(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = MUser.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(operation_description="this part is for convinent and should be ommited in the operation", operation_summary="reciving users informations")
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @swagger_auto_schema(operation_description="if you just send your phone number tou will recive a code and if you send your phone number and that password you recived you will be registered", operation_summary="registering with phone number")
    def post(self, request, *args, **kwargs):
        if 'password' in request.data.keys():
            if redis.get(request.data['phonenumber']) == request.data['password']:
                self.create(request, *args, **kwargs)
            else:
                return Response(status=400)
        else:
            ran = randint(10000, 99999)
            try:
                print(request.data['phonenumber'], ran)
                redis.set(request.data['phonenumber'], ran)
                redis.expire(request.data['phonenumber'], 1000)
                return Response(status=200)
            except:
                return Response(status=400)

    def create(self, request, *args, **kwargs):
        user = MUser.objects.create_user(
            username=request.data['phonenumber'], phonenumber=request.data['phonenumber'])
        user.set_unusable_password()
        user.save()
        # serializer = self.get_serializer(user)
        # serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_201_CREATED)

    def perform_create(self, user):
        return Response(status=200)


class OtpRequest(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):

    # permission_classes = (IsAuthenticated,)
    serializer_class = MUser
    QuerySet = Order.objects.all()

    @swagger_auto_schema(operation_description="if you send your phone number you will recieve a password that you can login with it", operation_summary="request for otp")
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        self.user = MUser.objects.get(phonenumber=kwargs['phonenumber'])
        if self.user:
            ran = randint(10000, 99999)
            try:
                print(kwargs['phonenumber'], ran)
                redis.set(self.user.id, ran)
                redis.expire(self.user.id, 10000)
                return Response(status=200)
            except:
                return Response(status=400)
        else:
            return Response(status=400)


class OtpLogin(object):
    def authenticate(self, request, username=None, password=None, **kwargs):
        my_user_model = get_user_model()
        try:
            user = my_user_model.objects.get(phonenumber=username)
            if redis.get(user.id) == password:
                return user  # return user on valid credentials
        except my_user_model.DoesNotExist:
            return None  # return None if custom user model does not exist
        except:
            return None  # return None in case of other exceptions

    def get_user(self, user_id):
        my_user_model = get_user_model()
        try:
            return my_user_model.objects.get(pk=user_id)
        except my_user_model.DoesNotExist:
            return None
