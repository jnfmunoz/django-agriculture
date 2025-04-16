from django.urls import path
from .views import SignUpView, ProfileUpdateView, ProfileDetailView, UserUpdateView

registration_patterns = ([
    path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<str:username>/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('user/<str:username>/update/', UserUpdateView.as_view(), name='user_update'),

], 'registration')
