from django.contrib.auth.models import User
from django.db import models


class MyUser(models.Model):
    user = models.OneToOneField(User)
    display_name = models.CharField(max_length=50)
    #picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)

# Create your models here.
