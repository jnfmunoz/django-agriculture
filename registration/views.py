from .forms import UserCreationForm, ProfileForm, UserForm
from django.views.generic import CreateView, DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms
from .models import Profile
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from blog.forms import PostForm
from blog.models import Post

User = get_user_model();

# Create your views here.
class SignUpView(CreateView):
    
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name ='registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'
    
    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real
        form.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder':'First Name'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':'Last Name'})
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':'Username'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder':'Email address'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder':'Password'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder':'Repeat password'})

        return form

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile 
    template_name = 'registration/profile/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self):
        username = self.kwargs.get('username')

        # Public profile
        if username:
            user = get_object_or_404(User, username=username)
            profile, _ = Profile.objects.get_or_create(user=user)

            return profile
        
        # Private profile
        user = self.request.user
        profile, _ = Profile.objects.get_or_create(user = user)
        return profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        profile_user = self.object.user
        request_user = self.request.user

        context["is_owner"] = (
            request_user.is_authenticated and request_user == profile_user
        )

        context["user_posts"] = (
            Post.objects
                .filter(author=profile_user)
                .order_by("-created_at")
        )

        if context["is_owner"]:
            context["form"] = PostForm

        return context

class ProfileUpdateView(LoginRequiredMixin, UpdateView):

    form_class = ProfileForm
    success_url = reverse_lazy('profile_detail')
    template_name = 'registration/profile/profile_update_form.html'

    def get_object(self, *args, **kwargs):
        
        username = self.kwargs.get('username')

        if username == self.request.user.username:
            profile, created = Profile.objects.get_or_create(user=self.request.user)
            return profile
        else:
            raise PermissionDenied("You do not have permission to edit this profile.")
    
    def get_success_url(self):
        return reverse_lazy('registration:profile_detail', kwargs={'username': self.request.user.username})

class UserUpdateView(LoginRequiredMixin, UpdateView):

    form_class = UserForm
    success_url = reverse_lazy('profile_detail')
    template_name = 'registration/user/user_update_form.html'

    def get_object(self, queryset=None,*args, **kwargs):
        return self.request.user
        
    def form_invalid(self, form):
        print("❌ Formulario inválido. Errores:", form.errors)
        return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('registration:profile_detail', kwargs={'username': self.request.user.username})
    
@login_required
def redirect_to_profile(request):
    return redirect('registration:profile_detail', username=request.user.username)
