from django.urls import path
from .views import (CommentCreateView, CommentDeleteView)

comment_patterns = ([
    path('post/<int:pk>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:pk>/delete/', CommentDeleteView.as_view(), name="comment_delete"),    
], 'comments')

