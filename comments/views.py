from django.shortcuts import get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
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
        post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
        form.instance.post = post
        form.instance.author = self.request.user

        parent_id = self.request.POST.get('parent_id')
        if parent_id:
            form.instance.parent = get_object_or_404(Comment, pk=parent_id)

        self.object = form.save()

        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            html = render_to_string(
                'blog/partials/comment_item.html', 
                {'comment': self.object, 'user': self.request.user},
                request=self.request
            )

            return JsonResponse({'html': html})

        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', kwargs={'pk': self.kwargs.get('pk')})
    
class CommentDeleteView(DeleteView):
    model = Comment
    
    def post(self, request, *args, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs['pk'])

        comment.delete()

        return JsonResponse({
            'success': True,
            'comment_id': comment.id
        })

