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

class PostCreateView(CreateView):

    model = Post
    form_class = PostForm
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        print("❌ Formulario inválido. Errores:", form.errors)
        return super().form_invalid(form)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = False
        context["form_action"] = reverse_lazy("blog:post_create")
        context["post"] = None
        return context

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
    template_name = "blog/post_form.html"

    def get_success_url(self):
        return reverse_lazy(
            "registration:profile_detail",
            kwargs={"username": self.request.user.username}
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_update"] = True
        context["post"] = self.object
        context["form_action"] = reverse_lazy(
            "blog:post_update",
            kwargs={"pk": self.object.pk}
        )
        return context

    # POST válido
    def form_valid(self, form):
        self.object = form.save()

        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})

        return super().form_valid(form)

    # POST inválido
    def form_invalid(self, form):
        if self.request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse(
                {"success": False, "errors": form.errors},
                status=400
            )
        return super().form_invalid(form)


