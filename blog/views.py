from django.shortcuts import redirect, render

from blog.forms import BoardForm
from .models import Post, Games
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.
def blog(request):
    page = request.GET.get('page', '1')  # 페이지
    postlist = Post.objects.all().order_by('-timestamp')

    paginator = Paginator(postlist, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'postlist': page_obj}

    return render(request, 'blog/index.html', context)

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required(login_url='users:login')
def new_post(request):
    form = BoardForm()
    return render(request, 'blog/new_post.html', {'form': form})

@login_required(login_url='users:login')
def upload_create(request):
    new_article = Post.objects.create(
        postname = request.POST['postname'],
        contents = request.POST['contents'],
        author = request.user,
        mainphoto = request.FILES.get('mainphoto')
    )

    new_article.save()

    form = BoardForm(request.POST)
    if form.is_valid():
        tags = form.cleaned_data.get('game').split(',')
        for tag in tags:
            if not tag : 
                continue
            else:
                tag_ = tag.strip()
                new_game = Games(game=tag_)
                new_game.save()
                new_article.game.add(new_game)
    
    return render(request, 'blog/post_detail.html', {'post': new_article})
   

@login_required(login_url='users:login')
def remove_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author != request.user:
        messages.error(request, '삭제 권한이 없습니다.')
        return redirect('blog:post_detail', pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('/blog')
    return render(request, 'blog/remove_post.html', {'Post': post})

