from django.shortcuts import get_object_or_404, redirect, render
from .models import Post, Like
from .forms import CommentForm, PostForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status="pb")
    context =  {
        "posts" : posts
    }
    return render(request, "blogapp/post_list.html", context)
    
@login_required
def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)    
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request,"Post created successfully!" )
            return redirect("blogapp:list")

    context = {
        "form": form
    }
    return render(request, "blogapp/post_create.html", context )


def post_detail(request, slug):
    post = Post.objects.get(slug = slug)
    form = CommentForm()
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post =  post
            comment.save()
            return redirect("blogapp:detail", slug=slug)
            #return redirect(request.path)       
    context = {
        "post": post,
        "form":form
         }
    return render(request, "blogapp/post_detail.html", context)

@login_required   
def post_update(request, slug):
    post = Post.objects.get(slug = slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if request.user != post.author:
        messages.warning(request,"You are not a writer of this post!" )
        return redirect("blogapp:list")
    if form.is_valid():
        form.save()
        messages.success(request,"Post updated successfully!" )
        return redirect("blogapp:list")

    context = {
        "post" : post,
        "form": form

    }
    return render(request, "blogapp/post_update.html", context)

@login_required   
def post_delete(request, slug):
    post = Post.objects.get(slug = slug)
    if request.user != post.author:
        messages.warning(request,"You are not a writer of this post!" )
        return redirect("blogapp:list")
    if request.method == "POST":
        post.delete()
        messages.success(request,"Post deleted successfully!" )
        return redirect("blogapp:list")
    return render(request, "blogapp/post_delete.html", {"post" : post})

@login_required()
def like(request, slug):
    if request.method == "POST":
        obj = get_object_or_404(Post, slug=slug)
        like_qs = Like.objects.filter(user=request.user, post=obj)
        if like_qs.exists():
            like_qs[0].delete()
        else:
            Like.objects.create(user=request.user, post=obj)
        return redirect("blogapp:detail", slug=slug)
    return redirect("blogapp:detail", slug=slug)