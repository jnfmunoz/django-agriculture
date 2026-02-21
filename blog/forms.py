from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from .validators import (NotOnlyNumbersValidator, MinMaxLengthValidator, NotEmptyValidator)

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

    def _validate_text_field(self, value, field_name, min_length=None, max_length=None, required=False):
        value = (value or "").strip()

        if required:
            NotEmptyValidator(field_name)(value)
        
        if value:
            MinMaxLengthValidator(
                min_length=min_length,
                max_length=max_length,
                field_name=field_name,
            )(value)
            NotOnlyNumbersValidator(field_name)(value)
            
        return value

    def clean_title(self):    
        return self._validate_text_field(
            self.cleaned_data.get('title'),
            field_name="El título",
            min_length=5,
            max_length=50,
            required=True,
        )    

    def clean_subtitle(self):
        return self._validate_text_field(
            self.cleaned_data.get('subtitle'),
            field_name="El subtítulo",
            min_length=5,
            max_length=50,
            required=True,
        )

    def clean_relevant_text(self):
        return self._validate_text_field(
            self.cleaned_data.get('relevant_text'),
            field_name="El texto relevante",
            min_length=5,
            max_length=50,
        )
    
    def clean_introduction(self):
        return self._validate_text_field(
            self.cleaned_data.get('introduction'),
            field_name="La introducción",
            min_length=5,
            max_length=500,
        )
    
    def clean_body_text(self):
         return self._validate_text_field(
            self.cleaned_data.get('body_text'),
            field_name="El cuerpo",
            min_length=5,
            max_length=1000,
        )

    def clean_conclusion(self):
         return self._validate_text_field(
            self.cleaned_data.get('conclusion'),
            field_name="La conclusión",
            min_length=5,
            max_length=500,
        )

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

        return cleaned_data