from django.shortcuts import redirect, render
from .models import Post
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'main/index.html')

def blog(request):
    page = request.GET.get('page', '1')  # 페이지
    postlist = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(postlist, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'postlist': page_obj}

    return render(request, 'main/blog.html', context)

def posting(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'main/posting.html', {'post': post})

@login_required(login_url='users:login')
def new_post(request):
    if request.method == 'POST':
        if request.POST['mainphoto']:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                mainphoto=request.POST['mainphoto'],
                author = request.user,
            )
        else:
            new_article=Post.objects.create(
                postname=request.POST['postname'],
                contents=request.POST['contents'],
                author = request.user,
                #mainphoto=request.POST['mainphoto'],
            )
        return render(request, 'main/posting.html', {'post': new_article})
    else:
        return render(request, 'main/new_post.html')

def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog')
    return render(request, 'main/remove_post.html', {'Post': post})

