from django.urls import path
from .views import *

app_name = 'posts'

urlpatterns = [
    path('', posts_list, name='post_list'),
    path('<int:post_id>/comments/', add_comment, name='add_comment'),
    path('profile_page/<str:username>/', profile_page, name='profile_page'),
    path('explore/', explore_posts, name='explore'),
    path('add_post/', create_post, name='add-post'),
    path('reels/', reels_list, name='reels'),
    path('like/<int:post_id>/', like_post, name='like_post'),
]
