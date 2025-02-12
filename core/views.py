from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class HomePageView(TemplateView):
    
    template_name = "index.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    

class AboutUsPageView(TemplateView):
    
    template_name = "about.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

class ServicesPageView(TemplateView):

    template_name = "services.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

