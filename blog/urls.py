from django.urls import path
from .views import (PostListView, PostDetailView, PostCreateView, PostDeleteView)

blog_patterns = ([
    path('', PostListView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
], 'blog')
