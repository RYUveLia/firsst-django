from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    postname = models.CharField(max_length=50)
    contents = models.TextField()
    mainphoto = models.ImageField(null = True, blank=True)
    timestamp = models.DateTimeField(default=timezone.now())

    def __str__(self):
        return self.postname