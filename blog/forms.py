from django import forms
from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'relevant_text','content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Título'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Subtítulo'}),
            'relevant_text': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 2, 'placeholder': 'Texto relevante'}),
            'content': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 6, 'placeholder': 'Contenido del post'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'}),            

        }
