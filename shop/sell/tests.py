from django.http import request
from django.test import TestCase
from rest_framework import status

# Create your tests here.
# from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from django.urls import reverse
from auser.models import *
from post.models import *
from .models import *
from model_mommy import mommy

# User = get_user_model()


class TestPost(APITestCase, TestCase):

    def setUp(self):
        # user = User(username='dev', password='123')
        # user.save()
        # post1 = Post(title='post title1', creator=user, published=True)
        # post1.save()
        # post2 = Post(title='post title2', creator=user)
        # post2.save()
        # post3 = Post(title='post title3', creator=user, published=True)
        # post3.save()

        self.user_shop = mommy.make(MUser, user_type='shop')
        self.user_costumer = mommy.make(MUser, user_type='costumer')
        self.shop = mommy.make(Shop, owner=self.user_shop)
        self.shop_basket = mommy.make(
            ShopBasket, costumer=self.user_costumer, shop=self.shop)
        self.product = mommy.make(
            ListOfComodity, shop=self.shop, remaining_stock=1000)
        self.order = mommy.make(
            Order, comodity=self.product, costumer=self.user_costumer, shop_basket=self.shop_basket, number=1)

    def test_one_order(self):
        # url = reverse('post_list')

        # resp = self.client.get(url)

        # self.assertEqual(resp.status_code, 200)
        print(self.product.price)
        print(self.shop_basket.total_price)

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

    def test_shop_type(self):
        url = reverse('sell:type_list')
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

    def test_shop_product(self):
        url = reverse('sell:product_list', kwargs={'shop_id': self.shop.id})
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)

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
                      'product_id': self.product.id, 'number': 1})
        self.client.force_authenticate(self.user_costumer)
        resp = self.client.post(url)
        self.assertEqual(resp.status_code, 200)
        url = reverse('sell:add_order', kwargs={
                      'product_id': self.product.id, 'number': 4000})
        resp = self.client.post(url)
        self.assertNotEqual(resp.status_code, 200)

    def test_delete_order(self):
        self.client.force_authenticate(self.user_costumer)
        url = reverse('sell:delete_order', args=[self.order.id])
        resp = self.client.delete(url)
        self.assertEqual(resp.status_code, 200)

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
