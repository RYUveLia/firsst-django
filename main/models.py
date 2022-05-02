from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    postname = models.CharField(max_length=50)
    contents = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now())
    mainphoto = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.postname