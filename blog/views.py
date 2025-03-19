from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import render

from .models import Post

# Create your views here.
class PostListView(ListView):

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["published_at"]
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(queryset)  
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class PostDetailView(DetailView):
    
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = 'post'

    def get_queryset(self):
        queryset = super().get_queryset()
        # print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)   
        post = self.get_object()
        context["comments"] = post.comments.all()
        context["comments_count"] = post.comments.count()     
        return context



