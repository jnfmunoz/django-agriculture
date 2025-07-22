from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
import re

# Create your models here.
class Post(models.Model):
    
    title = models.CharField(max_length=200, verbose_name='Title')
    subtitle = models.CharField(max_length=200, verbose_name='Subtitle')
    relevant_text = models.CharField(max_length=50, verbose_name='Relevant Text', null=True, blank=True)
    introduction = models.TextField(verbose_name='Introduction', null=True, blank=True)
    body_text = models.TextField(verbose_name='Body Text', null=True, blank=True)
    conclusion = models.TextField(verbose_name='Conclusion', null=True, blank=True)
    image = models.ImageField(verbose_name='Image', upload_to='posts', null=False, blank=False)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creation Date')
    updated_at = models.DateTimeField(auto_now=True, verbose_name = 'Edition Date')    

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

    def formatted_content(self):
        html_parts = []

        if self.introduction:
            intro_paragraphs = re.split(r'\n+', self.introduction.strip())
            html_parts.append("".join(f"<p>{p}</p>" for p in intro_paragraphs))

        if self.relevant_text:
            html_parts.append(f'<blockquote><p>{self.relevant_text}</p></blockquote>')

        if self.subtitle:
            html_parts.append(f'<h3 style="text-align:left">{self.subtitle}</h3>')
        
        if self.body_text:
            body_paragraphs = re.split(r'\n+', self.body_text.strip())
            html_parts.append("".join(f"<p>{p}</p>" for p in body_paragraphs))

        if self.conclusion:
            conclusion_paragraphs = re.split(r'\n+', self.conclusion.strip())
            html_parts.append("".join(f"<p>{p}</p>" for p in conclusion_paragraphs))

        return "".join(html_parts)
