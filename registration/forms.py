from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserCreationFormWithEmail(UserCreationForm):

    email = forms.EmailField(required=True, help_text="Required, 254 characters for maximum length.")

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

class ProfileForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['profile_photo', 'occupation', 'bio', 'facebook', 'instagram', 'linkedin', 'twitter']
        widgets = {
            'profile_photo': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),
            'occupation': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 1, 'placeholder': 'Occupation'}),
            'bio': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 6, 'placeholder': 'Biography'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control mt-3', 'rows':3, 'placeholder':'Facebook'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control mt-3', 'rows':3, 'placeholder':'Instagram'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control mt-3', 'rows':3, 'placeholder':'Linkedin'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control mt-3', 'rows':3, 'placeholder':'Twitter'}),

        }

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email'] #, 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email
