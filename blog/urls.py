from django.urls import path
from .views import BlogPageView

urlpatterns = [
    path('', BlogPageView.as_view(), name='blog'),

]