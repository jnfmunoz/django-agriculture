"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import (HomePageView, AboutUsPageView, ServicesPageView,
                    TestimonialsPageView, BlogPageView, ContactPageView)

urlpatterns = [
    path('', HomePageView.as_view(), name="index"),
    path('about/', AboutUsPageView.as_view(), name="about"),
    path('services/', ServicesPageView.as_view(), name="services"),
    path('testimonials/', TestimonialsPageView.as_view(), name="services"),
    path('blog/', BlogPageView.as_view(), name="services"),
    path('contact/', ContactPageView.as_view(), name="services"),


    path('admin/', admin.site.urls),
]
