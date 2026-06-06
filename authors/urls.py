from django.urls import path
from . import views

app_name = 'authors'

urlpatterns = [
    path('', views.feed_view, name='feed'),
    path('p/<str:username>/', views.profile_view, name='profile'),
    path('api/post/<int:post_id>/', views.post_detail_json, name='post_detail_json'),
    path('api/comment/add/', views.add_comment_json, name='add_comment_json'),
]
