from django.urls import  path, include
from .views import entryPost,create_user,entry_list_view_item_detail,entry_list_view,entry_list_view_item,entry_list_update_item,entry_list_delete_item,entry_list_create_item,like_entry
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'userapi'
urlpatterns = [
    path('', entry_list_view, name='detail list'),
    path('list', entryPost.as_view(), name='list'),
    path('entry/<int:id>/', entry_list_view_item_detail, name='detail list item'),
    path('entry/<int:id>/update', entry_list_update_item, name='update'),
    path('entry/<int:id>/delete', entry_list_delete_item, name='delete'),
    path('entry/likes', like_entry, name='like'),
    path('entry/create', entry_list_create_item, name='create'),
    path('user/register', create_user, name='user registration'),
    path('user/login', obtain_auth_token, name='user login'),
]