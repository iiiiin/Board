from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Post
from .forms import PostForm, LoginForm, CustomUserCreationForm
# Create your views here.


# 사용자 회원가입 엔드포인트
def user_signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("post_list")
    else:
        form = CustomUserCreationForm()
    return render(request, "boardapp/signup.html", {"form":form})

# 사용자 로그인 엔드포인트
def user_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data["password"]
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list')
            else:
                messages.error(request, "잘못된 사용자명 또는 비밀번호입니다.")
    else:
        form = LoginForm()        
    return render(request, 'boardapp/login.html', {'form': form})

# 사용자 로그아웃 엔드포인트
def user_logout(request):
    logout(request)
    return redirect("post_list")


# 새로운 게시글을 생성하는 엔드포인트
@login_required(login_url="/board/login/")
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.id = request.user
            post.save()
            return redirect('post_detail', pk=post.postid)
    else:
        form = PostForm()
    return render(request, 'boardapp/post_form.html', {'form': form})

# 게시글 목록을 조회하는 엔드포인트
def post_list(request):
    posts = Post.objects.all().order_by('-postdate')
    return render(request, "boardapp/post_list.html", {'posts':posts})

# 특정 게시글을 조회하는 엔드포인트
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "boardapp/post_detail.html", {'post':post})

# 특정 게시글을 수정하는 엔드포인트
@login_required(login_url="/board/login/")
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.postid = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'board/post_form.html', {'form': form})

# 특정 게시글을 삭제하는 엔드포인트
@login_required(login_url="/board/login/")
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, "boardapp/post_confirm_delete.html", {'post':post})
