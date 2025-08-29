from django.urls import path
from .views import (CommentCreateView)

comment_patterns = ([
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create')
], 'comments')

