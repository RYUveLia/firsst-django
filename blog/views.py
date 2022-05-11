import datetime as dt
from email import message
from django.shortcuts import redirect, render
from django.test import modify_settings
from django.utils import timezone
from blog.forms import BoardForm
from .models import Post, Game
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
import json

# Create your views here.
def blog(request):
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')
    postlist = Post.objects.all().order_by('-timestamp')
    postlist = postlist.filter(
        Q(disclosure=True) | # False = 비공개 
        (Q(disclosure=False) & Q(modified__gte=timezone.now()))
    )

    if kw:
        postlist = postlist.filter(
            Q(postname__icontains=kw) |  # 제목 검색
            Q(contents__icontains=kw) |  # 내용 검색            
            Q(author__username__icontains=kw) |  # 글쓴이 검색
            Q(game__name=kw)
        ).distinct()

    paginator = Paginator(postlist, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'postlist': page_obj, 'page': page, 'kw': kw}

    return render(request, 'blog/index.html', context)

def post_detail(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author == request.user:
        return render(request, 'blog/post_detail.html', {'post': post})
    elif post.disclosure == True:
        return render(request, 'blog/post_detail.html', {'post': post})
    elif post.disclosure == False and post.modified >= timezone.now():
        return render(request, 'blog/post_detail.html', {'post': post})
    else:
        messages.error(request, '권한이 없습니다.')
        return redirect('/blog')
        

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
        mainphoto = request.FILES.get('mainphoto'),
        modified = timezone.now(),
        timestamp = timezone.now(),
        disclosure = json.loads(request.POST['chk_info'].lower())
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
                
                new_game, created = Game.objects.get_or_create(name=tag_)
                if created == True:
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

@login_required(login_url='users:login')
def allow_post(request, pk):
    post = Post.objects.get(pk=pk)
    if post.author != request.user:
        messages.error(request, '공개 권한이 없습니다.')
        return redirect('blog:post_detail', pk=pk)
    
    if request.method == 'POST':
        post.modified = timezone.now() + dt.timedelta(minutes = 10)
        post.save()
        return redirect('/blog')

    return render(request, 'blog/allow_post.html', {'Post': post})