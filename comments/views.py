from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .models import Comment
from blog.models import Post


# Create your views here.
class CommentListView(ListView):
    
    model = Comment
    context_object_name = 'comments'

class CommentCreateView(CreateView):    
    
    model = Comment
    fields = ['content']

    def form_valid(self, form):
        post_id = self.kwargs.get('pk')
        post = get_object_or_404(Post, pk=post_id)

        form.instance.post = post
        form.instance.author = self.request.user

        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            parent_comment = Comment.objects.get(id=parent_id)
            form.instance.parent = parent_comment

    
        return super().form_valid(form)
    
    def get_success_url(self):
        return super().get_success_url('blog:post_detail', kwargs={'pk': self.kwargs.get('pk')})
    