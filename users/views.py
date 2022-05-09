from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import get_object_or_404, render, redirect
from users.forms import UserForm
from blog.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)  # 사용자 인증
            login(request, user)  # 로그인
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

@login_required(login_url='users:login')
def detail(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk)

    context = {
        'user': user
    }

    return render(request, 'users/detail.html', context)

@login_required(login_url='users:login')
def mypost(request, pk):

    User = get_user_model()
    user = get_object_or_404(User, pk=pk)

    page = request.GET.get('page', '1')  # 페이지
    post = Post.objects.all().order_by('-timestamp')
    postlist = post.filter(author=user)

    paginator = Paginator(postlist, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)
    
    context = {'postlist': page_obj}

    return render(request, 'users/mypost.html', context)