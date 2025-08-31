from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.urls import reverse_lazy
from .models import Post
from comments.models import Comment
from .forms import PostForm

# Create your views here.
class PostListView(ListView):

    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    ordering = ["created_at"]
    paginate_by = 6

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     # print(queryset)  
    #     return queryset
    
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Lista de comentarios del post
    #     context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
    #     return context

# class PostDetailView(DetailView):
    
#     model = Post
#     template_name = "blog/post_detail.html"
#     context_object_name = 'post'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['comments'] = Comment.objects.filter(post=self.object).order_by('-created')
#         return context

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        return context


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

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = "blog/partials/post_update_form.html"  # solo el form

    # Definir la URL de éxito para POST normal
    def get_success_url(self):
        return reverse_lazy(
            'registration:profile_detail',
            kwargs={'username': self.request.user.username}
        )

    # GET AJAX: devuelve solo el form renderizado
    def get(self, request, *args, **kwargs):
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            self.object = self.get_object()
            context = {'form': self.get_form(), 'post': self.object}
            return render(request, self.template_name, context)
        return super().get(request, *args, **kwargs)

    # POST AJAX: si es válido, devolver JSON; si no, devolver errores
    def form_valid(self, form):
        response = super().form_valid(form)  # guarda el form
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        return response

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return super().form_invalid(form)

