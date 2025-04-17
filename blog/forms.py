from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'relevant_text','content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Title'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Subtitle'}),
            'relevant_text': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 2, 'placeholder': 'Relevant Text'}),
            'content': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 6, 'placeholder': 'Post Content'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),            

        }
