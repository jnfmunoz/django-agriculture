from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from .models import Post
from .validators import NotOnlyNumbersValidator

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'subtitle', 'relevant_text','introduction', 'body_text', 'conclusion','image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Title'}),
            'subtitle': forms.TextInput(attrs={'class': 'form-control mt-3', 'placeholder': 'Subtitle'}),
            'relevant_text': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 2, 'placeholder': 'Relevant Text'}),
            'introduction': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 6, 'placeholder': 'Post Introduction'}),
            'body_text': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 10, 'placeholder': 'Body Text'}),
            'conclusion': forms.Textarea(attrs={'class': 'form-control mt-3', 'rows': 8, 'placeholder': 'Conclusion'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file mt-3'})
        }

    def clean_title(self):
        title = self.cleaned_data.get('title', '').strip()
        if len(title) < 5:
            raise ValidationError("El título debe tener al menos 5 caracteres.")
        if len(title) > 50:
            raise ValidationError("El título no puede superar los 50 caracteres.")
        NotOnlyNumbersValidator("El título")(title)
        return title
    
    def clean_subtitle(self):
        subtitle = self.cleaned_data.get('subtitle', '').strip()
        if len(subtitle) < 5:
            raise ValidationError("El subtítulo debe tener al menos 5 caracteres.")
        if len(subtitle) > 50:
            raise ValidationError("El subtítulo no puede superar los 50 caracteres.")
        NotOnlyNumbersValidator("El título")(subtitle)
        return subtitle    
    
    def clean_relevant_text(self):
        relevant_text = self.cleaned_data.get('relevant_text', '').strip()
        if relevant_text: 
            if len(relevant_text) < 5:
                raise ValidationError("El texto relevante debe tener al menos 5 caracteres.")
            if len(relevant_text) > 50:
                raise ValidationError("El texto relevante no puede superar los 50 caracteres.")
            NotOnlyNumbersValidator("El texto relevante")(relevant_text)
        return relevant_text
    
    def clean_introduction(self):
        introduction = self.cleaned_data.get('introduction', '').strip()
        if introduction:
            if len(introduction) < 5:
                raise ValidationError("La introducción debe tener al menos 5 caracteres.")
            if len(introduction) > 50:
                raise ValidationError("La introducción no puede superar los 50 caracteres.")
            NotOnlyNumbersValidator("La introducción")(introduction)        
        return introduction
    
    def clean_body_text(self):
        body_text = self.cleaned_data.get('body_text', '').strip()
        if body_text:
            if len(body_text) < 5:
                raise ValidationError("El cuerpo debe tener al menos 5 caracteres.")
            if len(body_text) > 50:
                raise ValidationError("El cuerpo no puede superar los 50 caracteres.")
            NotOnlyNumbersValidator("El cuerpo")(body_text)   
        return body_text

    def clean_conclusion(self):
        conclusion = self.cleaned_data.get('conclusion', '').strip()
        if conclusion:
            if len(conclusion) < 5:
                raise ValidationError("La conclusión debe tener al menos 5 caracteres.")
            if len(conclusion) > 500:
                raise ValidationError("La conclusión no puede superar los 500 caracteres.")
            NotOnlyNumbersValidator("La conclusión")(conclusion)
        return conclusion

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title', '').strip()
        subtitle = cleaned_data.get('subtitle', '').strip()
        introduction = cleaned_data.get('introduction', '').strip()
        body_text = cleaned_data.get('body_text', '').strip()
        conclusion = cleaned_data.get('conclusion', '').strip()
        image = cleaned_data.get('image')

        if title and subtitle and title == subtitle:
            self.add_error('subtitle', "El subtítulo no puede ser igual al título.")

        if not any([introduction, body_text, conclusion]):
            raise ValidationError(
                "El post debe contener al menos una sección de texto "
                "(introducción, cuerpo o conclusión)."
            )

        if not image:
            self.add_error('image', "La imagen es obligatoria.")
