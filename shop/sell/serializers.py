from django.contrib.auth import get_user_model
from rest_framework import serializers

from auser.models import *
from .models import *
from post.models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MUser
        fields = ['id', 'username', 'email', 'password', 'phonenumber']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['image', 'address', 'first_name',
                  'last_name', 'profession', 'interest']

    # image = models.ImageField(
    #     upload_to='uploads', null=True, blank=True)
    # address = models.CharField(max_length=255)
    # firs_name = models.CharField(max_length=255)
    # firs_name = models.CharField(max_length=255)
    # profession = models.CharField(max_length=255)
    # interest = models.CharField(max_length=255)
    # costumer = models.OneToOneField(
    #     MUser, on_delete=models.CASCADE, null=True, blank=True)


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username']


# class PostSerializer(serializers.ModelSerializer):
#     tag = TagSerializer()
#     creator = UserSerializer()

#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'created', 'tag', 'creator']


# class PostCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Post
#         fields = ['title', 'tag']


# class PostDetailSerializer(serializers.ModelSerializer):
#     # creator = UserSerializer()
#     # tags = TagSerializer(many=True)
#     # tag = TagSerializer()

#     class Meta:
#         model = Post
#         fields = ['id', 'title', 'created', 'tags', 'tag']


# class PostUpdateSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Post
#         fields = ['title', 'tag']
