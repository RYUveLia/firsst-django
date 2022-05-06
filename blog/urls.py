from django.urls import path
from blog.views import *

app_name = "blog"
urlpatterns = [
    path('', blog),
    path('<int:pk>', posting, name='posting'),
    path('new_post/', new_post),
    path('<int:pk>/remove/', remove_post),
    path('upload_create/', upload_create ,name="upload_create"),
]