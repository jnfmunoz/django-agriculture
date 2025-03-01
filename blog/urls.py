from django.urls import path
from .views import PublicPostListView, PublicPostDetailView

urlpatterns = [
    path('', PublicPostListView.as_view(), name='post-list'),
    path('<int:pk>/', PublicPostDetailView.as_view(), name='post-detail'),
]