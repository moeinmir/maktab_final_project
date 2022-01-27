from django.http import request
from django.test import TestCase
import redis
from rest_framework import status

# Create your tests here.
# from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from auser.models import *
from post.models import *
from .models import *
from model_mommy import mommy
from sell.views import redis
# User = get_user_model()


class TestPost(APITestCase, TestCase):

    def setUp(self):

        self.user_shop = mommy.make(MUser, user_type='shop')
        self.category = mommy.make(Category)
        self.user_costumer = mommy.make(
            MUser, user_type='costumer', phonenumber="+989110000000")
        self.shop = mommy.make(Shop, owner=self.user_shop,
                               status='confirmed', category=self.category)
        self.shop_basket = mommy.make(
            ShopBasket, costumer=self.user_costumer, shop=self.shop)
        self.product = mommy.make(
            ListOfComodity, shop=self.shop, remaining_stock=1000, __quantity=10)
        self.order = mommy.make(
            Order, comodity=self.product, costumer=self.user_costumer, shop_basket=self.shop_basket, number=1)

    def test_one_order(self):
        self.assertEqual(self.product.price, self.shop_basket.total_price)

    def test_register(self):
        url = reverse('sell:user_register')
        data = {'username': 'user1',
                'password': 'pass1'
                }
        resp = self.client.post(url, data=data)
        user = MUser.objects.all()
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(len(user), 3)
        data = {'username': 'user2',
                'password': 'pass2',
                'email': 'email@gmail.com'
                }
        resp = self.client.post(url, data=data)
        user = MUser.objects.last()
        print(user)
        self.assertEqual(user.email, 'email@gmail.com')

    def test_profile(self):
        url = reverse('sell:profile_register')
        data = {'first_name': 'name1'}
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.post(url, data=data)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(Profile.objects.get(
            costumer=self.user_costumer).first_name, 'name1')
        resp = self.client.get(url)
        self.assertEqual(resp.data['first_name'], 'name1')
        data = {'first_name': 'name2'}
        resp = self.client.put(url, data=data)
        resp = self.client.get(url)
        self.assertEqual(resp.data['first_name'], 'name2')

    def test_shop_list(self):
        url = reverse('sell:shop_list')
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        a = len(Shop.objects.filter(status='confirmed'))
        b = len(resp.data)
        self.assertEqual(a, b)

    def test_shop_type(self):
        url = reverse('sell:type_list')
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        a = len(Category.objects.all())
        b = len(resp.data)
        self.assertEqual(a, b)

    def test_shop_product(self):
        url = reverse('sell:product_list', kwargs={'shop_id': self.shop.id})
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        a = len(ListOfComodity.objects.filter(
            shop=self.shop, status='existing'))
        b = len(resp.data)
        self.assertEqual(a, b)

    def test_add_shop_basket(self):
        url = reverse('sell:add_shop_basket', kwargs={
                      'product_id': self.product.id})
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        for i in range(10):
            resp = self.client.post(url)
        number_of_open_basket = ShopBasket.objects.filter(
            status='processing', costumer=self.user_costumer)
        self.assertEqual(len(number_of_open_basket), 1)

    def test_add_order(self):
        url = reverse('sell:add_order', kwargs={
                      'product_id': self.product.id, 'number': 3})
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        url = reverse('sell:add_order', kwargs={
                      'product_id': self.product.id, 'number': 40000})
        resp = self.client.post(url)
        self.assertNotEqual(resp.status_code, 200)
        a = ShopBasket.objects.get(costumer=self.user_costumer).total_price
        b = self.product.price*4
        self.assertEqual(a, b)

    def test_delete_order(self):
        a = len(Order.objects.filter(shop_basket=self.shop_basket))
        self.client.force_authenticate(self.user_costumer)
        url = reverse('sell:delete_order', args=[self.order.id])
        resp = self.client.delete(url)
        b = len(Order.objects.filter(shop_basket=self.shop_basket))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(a-b, 1)

    def test_pay_shop_basket(self):
        self.client.force_authenticate(self.user_costumer)
        url = reverse('sell:pay_shop_basket', args=[self.shop_basket.id])
        resp = self.client.put(url)
        self.assertEqual(resp.status_code, 200)

    def test_list_shop_basket(self):
        self.client.force_authenticate(self.user_costumer)
        url = reverse('sell:shop_basket_costumer_list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        a = len(ShopBasket.objects.filter(
            status='payed', costumer=self.user_costumer))
        b = len(resp.data)
        self.assertEqual(a, b)

    def test_otp(self):
        # self.client.force_authenticate(self.user_costumer)
        url = reverse('sell:otp_request', kwargs={
                      'phonenumber': '+989110000000'})
        resp = self.client.post(url)
        a = redis.get(self.user_costumer.id)
        self.assertNotEqual(a, None)
        self.assertEqual(resp.status_code, 200)
