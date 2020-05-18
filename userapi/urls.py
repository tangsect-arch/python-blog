from django.urls import  path, include
from .views import  entry_list_view_item_detail,entry_list_view,entry_list_view_item,entry_list_update_item,entry_list_delete_item,entry_list_create_item,like_entry
from rest_framework import routers

app_name = 'userapi'
urlpatterns = [
    path('', entry_list_view, name='detail list'),
    # path('<int:id>/', entry_list_view_item, name='detail list item'),
    path('<int:id>/', entry_list_view_item_detail, name='detail list item'),
    path('<int:id>/update', entry_list_update_item, name='update'),
    path('<int:id>/delete', entry_list_delete_item, name='delete'),
    path('likes', like_entry, name='like'),
    path('create', entry_list_create_item, name='create'),
]