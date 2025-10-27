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
from comments.forms import CommentForm

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
        context['form'] = CommentForm()  # <-- ESTA LÍNEA ES LA CLAVE
        return context


    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()
            return redirect("blog:post_detail", pk=self.object.pk)
        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)

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
'''

class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created')
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = self.object
            comment.author = request.user
            comment.save()

            # Si es AJAX, devolvemos solo el comentario recién agregado
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                context = {'comment': comment}
                return JsonResponse({
                    'author': comment.author.get_full_name() or comment.author.username,
                    'content': comment.content,
                    'created': comment.created.strftime("%b %d, %Y"),
                    'profile_photo_url': comment.author.profile.profile_photo.url
                })
            
            # Si no es AJAX, redirigimos a la misma página
            return redirect("blog:post_detail", pk=self.object.pk)

        # Si el formulario no es válido, renderizamos la página con errores
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

'''

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

