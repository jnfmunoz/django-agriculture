from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post
from .forms import PostForm

# Create your views here.
class PostListView(ListView):

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["created_at"]
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

class PostCreateView(CreateView):

    model = Post
    # template_name = "blog/post_create_form.html"
    form_class = PostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("❌ Formulario inválido. Errores:", form.errors)
        return redirect(self.get_success_url())
    
    def get_success_url(self):
        return reverse_lazy('registration:profile_detail', kwargs={'username':self.request.user.username}) 

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    model = Post    

    def get_success_url(self):
        return reverse_lazy('registration:profile_detail', kwargs={'username':self.request.user.username}) 

    def test_func(self):
        
        post = self.get_object()
        return self.request.user == post.author

    '''
    def handle_no_permission(self):        
        messages.error(self.request, "No estás autorizado para eliminar este Post.")
        return redirect('post-list')
    '''

# class PostUpdateView(UpdateView):
    
#     model = Post
#     form_class = PostForm
#     # template_name = 'blog/post_update_form.html'
#     def get_success_url(self):
#         return reverse_lazy('registration:profile_detail', kwargs={'username':self.request.user.username}) 


class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        # Renderizar solo el formulario como fragmento
        return render(request, 'blog/partial_post_update_form.html', {'form': form, 'post': self.object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        else:
            return render(request, 'blog/partial_post_update_form.html', {'form': form, 'post': self.object})

    def get_success_url(self):
        return reverse_lazy('registration:profile_detail', kwargs={'username': self.request.user.username})