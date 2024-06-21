from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),

    path('inbox/', inbox, name='inbox'),
    path('<str:username>/', inbox, name='inbox'),

    path('edit/<str:username>/', edit_profile, name='edit-profile'),
]
