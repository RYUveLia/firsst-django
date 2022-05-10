from django.urls import path
from blog.views import *

app_name = "blog"
urlpatterns = [
    path('', blog, name='blog'),
    path('<int:pk>', post_detail, name='post_detail'),
    path('new_post/', new_post, name='new_post'),
    path('<int:pk>/remove/', remove_post),
    path('upload_create/', upload_create ,name="upload_create"),
]