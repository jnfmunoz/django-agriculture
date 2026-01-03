from django.db import models
from django.contrib.auth.models import User
from django.templatetags.static import static

# Create your models here.
class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_photo = models.ImageField(upload_to='profiles', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    occupation = models.CharField(max_length=200, null=True, blank=True)
    facebook = models.URLField(max_length=200, null=True, blank=True)
    instagram = models.URLField(max_length=200, null=True, blank=True)
    linkedin = models.URLField(max_length=200, null=True, blank=True)
    twitter = models.URLField(max_length=200, null=True, blank=True)

    def get_profile_photo_url(self):
        if self.profile_photo:
            return self.profile_photo.url
        return static('core/img/registration/no-avatar.jpg')

    def __str__(self):
        return f'Perfil de {self.user.first_name} {self.user.last_name}'


# .author.profile.get_profile_photo_url