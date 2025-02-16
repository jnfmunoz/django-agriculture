from django.urls import path
from .views import SignUpView, ProfileUpdateView, ProfileDetailView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', ProfileUpdateView.as_view(), name='profile'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),
]
