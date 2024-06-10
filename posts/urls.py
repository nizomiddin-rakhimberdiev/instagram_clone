from django.urls import path
from .views import *

app_name='posts'

urlpatterns = [
    path('', posts_list, name='post_list')
]