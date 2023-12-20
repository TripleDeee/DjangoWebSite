from django.urls import path
from .views import (post_list, post_detail, add_comment, register, logout_view, change_password, user_login, like_post)
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', post_list, name='post_list'),
    path('post/<int:pk>/', post_detail, name='post_detail'),
    path('post/<int:post_id>/comment/', add_comment, name='add_comment'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', user_login, name='login'),
    path('change-password/', change_password, name='change_password'),
    path('like_post/<int:post_id>/', like_post, name='like_post'),
]