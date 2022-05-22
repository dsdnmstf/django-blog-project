from django.shortcuts import redirect, render
from .models import Post
from .forms import PostForm
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
    
