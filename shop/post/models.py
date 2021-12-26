from django.db import models
from django.utils.text import slugify
import random
import string
from django.utils.text import slugify
from django.contrib.auth.models import User
# Create your models here.

BLOG_STATUS_CHOICE = (('Drafted', 'Drafted'), ('Published', 'Published'))


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_slugify(instance, slug):
    """
    checking if slug exist adding string to slug
    """
    model = instance.__class__
    unique_slug = slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = slug
        unique_slug += random_string_generator(size=4)
    return unique_slug


class Category(models.Model):
    category_name = models.CharField(max_length=72)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.category_name


class Tag(models.Model):
    tag_name = models.CharField(max_length=50)

    def __str__(self):
        return self.tag_name


class Post(models.Model):
    post_title = models.CharField(max_length=72)
    post_category = models.ManyToManyField(Category)
    post_content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    post_tag = models.ManyToManyField(Tag, blank=True, null=True)
    creator = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(
        upload_to='uploads', null=True, blank=True)
    created_on = models.DateField(auto_now_add=True, null=True, blank=True)
    update_on = models.DateField(auto_now=True, null=True, blank=True)
    status = models.CharField(
        max_length=10, choices=BLOG_STATUS_CHOICE, default='Drafted')
    post_summery = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.post_title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, slugify(self.post_title))
        super().save(*args, **kwargs)


class Comment(models.Model):
    comment_content = models.CharField(max_length=255)
    related_post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.comment_content
