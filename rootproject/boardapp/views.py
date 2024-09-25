from django.shortcuts import render
from .models import Post
# Create your views here.

def post_list(request):
    items = Post.objects.all()
    return render(request, "boardapp/item_list.html", {'items':items})