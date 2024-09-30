from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('/post/create/', views.post_create, name='post_create'),
    path('/post/<int:pk>/update/', views.post_update, name='post_update'),
    path('/post/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('/login/', views.user_login, name='user_login'),
    path('/logout/', views.user_logout, name='user_logout'),
    path('/signup/', views.user_signup, name='user_signup'),
]