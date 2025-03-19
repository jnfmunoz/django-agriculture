from django.db import models
from django.contrib.auth.models import User
from blog.models import Post

# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created'] 

    def __str__(self):
        return f'Comentario de {self.author.first_name} {self.author.last_name} en {self.post.title}'
