from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Title')
    subtitle = models.CharField(max_length=200, verbose_name='Subtitle')
    content = models.TextField(verbose_name='Content')
    image = models.ImageField(verbose_name='Image', upload_to='posts', null=True, blank=True)
    author = models.ForeignKey(User, verbose_name='Author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name = "Edition Date")
    published_at = models.DateTimeField(verbose_name="Published Date", default=now)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    