from django.urls import path

from post.views import *

app_name = 'post'

urlpatterns = [
    path('index/', post_index, name="index"),
    path('create/', post_create, name='create'),
    path('detail/<slug:slug>', post_detail, name="detail"), #postlary id-sy boyunca yuzlenip bolyar.meselem post/detail/2/
    path('update/<slug:slug>', post_update, name='update'),
    path('delete/<slug:slug>', post_delete, name='delete'),
]