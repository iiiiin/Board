from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .models import Post
from .forms import PostForm, LoginForm, CustomUserCreationForm
from django.http import JsonResponse
import json
# Create your views here.


# 사용자 회원가입 엔드포인트
def user_signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return JsonResponse({"message": "User created successfully", "user_id": user.email}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=405)

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
                return JsonResponse({"message": "Logged in successfully", "user_id": user.email})
            else:
                return JsonResponse({"error": "Invalid credentials"}, status=400)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=405)

# 사용자 로그아웃 엔드포인트
def user_logout(request):
    logout(request)
    return JsonResponse({"message": "Logged out successfully"})


# 새로운 게시글을 생성하는 엔드포인트
@login_required(login_url="/board/login/")
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.id = request.user
            post.save()
            return JsonResponse({"message": "Post created successfully", "post_id": post.postid}, status=201)
        else:
            return JsonResponse(form.errors, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=405)

# 게시글 목록을 조회하는 엔드포인트
def post_list(request):
    if request.method == "GET":
        posts = Post.objects.all().order_by('-postdate').values()
        post_list = []
        for post in posts:
            post_list.append({
                "postid": post["postid"],
                "title": post['title'],
                "content": post['content'],
                "user": post['id_id'],
                "created_at": post['postdate']
            })
        return JsonResponse(post_list, safe=False)
    return JsonResponse({"message": "Invalid request method"}, status=405)

# 특정 게시글을 조회하는 엔드포인트
def post_detail(request, pk):
    try:
        post = Post.objects.get(pk=pk)
        print(post)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.method == "GET":
        post_data = {
            "postid": post.postid,
            "title": post.title,
            "content": post.content,
            "user": post.id_id,
            "created_at": post.postdate,
        }
        return JsonResponse(post_data)
    return JsonResponse({"message": "Invalid request method"}, status=405)

# 특정 게시글을 수정하는 엔드포인트
@login_required(login_url="/board/login/")
def post_update(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.user != post.id:
        return JsonResponse({"error": "You are not authorized to edit this post"}, status=403)
    
    if request.method == "GET":
        data = {
            "id": post.postid,
            "title": post.title,
            "content": post.content,
            "author": post.id_id,
            "created_at": post.postdate.isoformat(),
        }
        print(data)
        return JsonResponse(data)
    
    elif request.method == "PUT":
        print(request.body)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)

        form = PostForm(data, instance=post)
        if form.is_valid():
            post = form.save()
            return JsonResponse({"message": "Post updated successfully", "post_id": post.id_id})
        else:
            return JsonResponse({"error": form.errors}, status=400)
    return JsonResponse({"message": "Invalid request method"}, status=405)
        

# 특정 게시글을 삭제하는 엔드포인트
@login_required(login_url="/board/login/")
def post_delete(request, pk):
    try:
        post = Post.objects.get(pk=pk)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)

    if request.user != post.id:
        return JsonResponse({"error": "You are not authorized to delete this post"}, status=403)

    if request.method == "DELETE":
        post.delete()
        return JsonResponse({"message": "Post deleted successfully"}, status=204)
    return JsonResponse({"message": "Invalid request method"}, status=405)
