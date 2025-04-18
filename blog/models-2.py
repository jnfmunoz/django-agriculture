from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import re

# Create your models here.
class Post(models.Model):
    
    title = models.CharField(max_length=200, verbose_name='Title')
    subtitle = models.CharField(max_length=200, verbose_name='Subtitle')
    relevant_text = models.CharField(max_length=50, verbose_name='Relevant Text', null=True, blank=True)
    content = models.TextField(verbose_name='Content')
    image = models.ImageField(verbose_name='Image', upload_to='posts', null=False, blank=False)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Edition Date')
    published_at =  models.DateTimeField(verbose_name='Published Date', default=now)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def formatted_content(self):
        paragraphs = re.split(r'\n+', self.content.strip())  # Divide el contenido en párrafos
        
        if not paragraphs:  
            return ""  # Si no hay contenido, retorna vacío
        
        first_two = "".join(f"<p>{p}</p>" for p in paragraphs[:3])  # Primeros 2 párrafos
        blockquote = f"<blockquote><p>{self.relevant_text}</p></blockquote>" if self.relevant_text else ""
        subtitle = f'<h3 style="text-align:left">{ self.subtitle }</h3>' 
        remaining = "".join(f"<p>{p}</p>" for p in paragraphs[2:])  # Resto de los párrafos

        return first_two + blockquote + subtitle + remaining  # Concatenar todo
    
    def count_paragraphs(self):
        return len(re.split(r'\n+', self.content.strip()))
    