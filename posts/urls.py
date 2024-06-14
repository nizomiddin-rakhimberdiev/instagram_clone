from django.urls import path
from .views import *

app_name='posts'

urlpatterns = [
    path('', posts_list, name='post_list'),
    path('<int:post_id>/comments/', add_comment, name='add_comment'),
]