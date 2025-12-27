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
from django.urls import path, include
from django.conf import settings
from .views import (HomePageView, AboutUsPageView, ServicesPageView,
                    TestimonialsPageView, ContactPageView)
from blog.urls import blog_patterns
from comments.urls import comment_patterns
from registration.urls import registration_patterns

urlpatterns = [
    path('', HomePageView.as_view(), name="index"),
    path('about/', AboutUsPageView.as_view(), name="about"),
    path('services/', ServicesPageView.as_view(), name="services"),
    path('testimonials/', TestimonialsPageView.as_view(), name="testimonials"),
    path('contact/', ContactPageView.as_view(), name="contact"),
       
    path('blog/', include(blog_patterns)),     
    path('comments/', include(comment_patterns), name="comments"),     
    
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    # path('accounts/', include('registration.urls')),
    path('accounts/', include(registration_patterns)),     

]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
