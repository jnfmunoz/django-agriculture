from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class UserCreationForm(UserCreationForm):

    first_name = forms.CharField(required=True, help_text="Required, 150 characters for maximum length.")
    last_name = forms.CharField(required=True, help_text="Required, 150 characters for maximum length.")
    email = forms.EmailField(required=True, help_text="Required, 254 characters for maximum length.")

    class Meta:
        model = User
        fields = ['first_name', 'last_name' , 'username', 'email', 'password1', 'password2']

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

    password1 = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(attrs={
            'class': 'form-control mt-3',
            'placeholder': 'New Password'
        }),
        required=False
    )

    password2 = forms.CharField(
        label = 'Repeat Password',
        widget = forms.PasswordInput(attrs={
            'class': 'form-control mt-3',
            'placeholder': 'Repeat New Password'
        }),
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder':'First name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder':'Last name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Email address'}),
        }
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("Passwords must match.")
        return password2
