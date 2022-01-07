from django.urls import path
from .views import *
from django.views.generic import TemplateView
from .views import CategoryListView

app_name = 'post'

urlpatterns = [

    path('post_list/', post_list, name='post_list'),
    path('post_details/<slug>', post_details),
    path('category/', CategoryListView.as_view(template_name='category_list_view.html')),
    path('category_details_view/<int:category_id>', category_details_view),
    path('register_form/', register_form, name='register_form'),
    path('post_form/', post_form, name='post_form'),
    #     path('comment_form/', comment_form, name='comment_form'),
    path('category_form_edit/<int:id>',
         category_form_edit, name='category_form_edit'),
    path('post_form_edit/<int:id>',
         post_form_edit, name='post_form_edit'),
    path('login/', mylogin, name='mylogin'),
    path('search/', search, name='search'),
    #     path('logout/', logout, name='logout')
    path('category_delete/<int:id>', category_delete, name='category_delete')
]
