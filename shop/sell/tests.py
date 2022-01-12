from django.http import request
from django.test import TestCase

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
        self.product = mommy.make(ListOfComodity, shop=self.shop)
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

        # self.assertEqual(len(user), 3)

    # def test_create_post(self):

    #     url = reverse('post_list')

    #     tag = Tag.objects.first()
    #     data = {
    #         'title': 'test title',
    #         'tag': tag.id
    #     }
    #     self.client.force_authenticate(self.user)

    #     resp = self.client.post(url, data=data)

    #     self.assertEqual(resp.status_code, 201)

    #     post = Post.objects.get(id=resp.data['id'])

    #     self.assertEqual(post.creator, self.user)
    #     self.assertFalse(post.published)

    # def test_update_post(self):
    #     post = Post(creator=self.user, title='test title', tag=Tag.objects.first())
    #     post.save()

    #     url = reverse('post_detail', kwargs={'id':post.id})
    #     new_title = "new title"
    #     data = {
    #         "title": new_title,
    #         "tag": Tag.objects.last().id
    #     }

    #     self.client.force_authenticate(self.user)
    #     resp = self.client.put(url, data)

    #     self.assertEqual(resp.status_code, 200)

    #     updated_post = Post.objects.get(id=post.id)
    #     self.assertEqual(updated_post.title, new_title)

    # def test_update_post_with_invalid_user(self):
    #     post = Post(creator=self.user, title='test title', tag=Tag.objects.first())
    #     post.save()

    #     url = reverse('post_detail', kwargs={'id': post.id})
    #     new_title = "new title"
    #     data = {
    #         "title": new_title,
    #         "tag": Tag.objects.last().id
    #     }

    #     another_user = mommy.make(User)
    #     self.client.force_authenticate(another_user)

    #     resp = self.client.put(url, data)

    #     self.assertEqual(resp.status_code, 400)
