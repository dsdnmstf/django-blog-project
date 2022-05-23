from django.shortcuts import redirect, render
from .models import Post
from .forms import CommentForm, PostForm
# Create your views here.
def post_list(request):
    posts = Post.objects.filter(status="pb")
    context =  {
        "posts" : posts
    }
    return render(request, "blogapp/post_list.html", context)

def post_create(request):
    form = PostForm()
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)    
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
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

def post_update(request, slug):
    post = Post.objects.get(slug = slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)
    if form.is_valid():
        form.save()
        return redirect("blogapp:list")

    context = {
        "post" : post,
        "form": form

    }
    return render(request, "blogapp/post_update.html", context)

def post_delete(request, slug):
    post = Post.objects.get(slug = slug)
    if request.method == "POST":
        post.delete()
        return redirect("blogapp:list")
    return render(request, "blogapp/post_delete.html", {"post" : post})
