from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Game(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    postname = models.CharField(max_length=128) # 업적명
    contents = models.TextField() # 한줄평
    
    mainphoto = models.ImageField(null = True, blank=True)
    timestamp = models.DateTimeField() #작성시간

    disclosure = models.BooleanField(default=False) # 기본적으로는 비공개
    modified = models.DateTimeField() # 공개날짜

    game = models.ManyToManyField(Game)
    
    def __str__(self):
        return self.postname