from email.policy import default
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
def user_directory_path(instance, filename):
    return "blog/{0}/{1}".format(instance.author.id, filename)

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta():
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class Post(models.Model):
    OPTIONS = (
        ("dr", "Draft"),
        ("pb", "Puplished")
    )
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to=user_directory_path, default="django.jpg")
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    puplish_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=OPTIONS, default="dr") 
    slug = models.SlugField(blank=True, unique=True)

    def __str__(self):
        return self.title

    def comment_count(self):
        return self.comment_set.all().count()
    
    def view_count(self):
        return self.postview_set.all().count()
    
    def like_count(self):
        return self.like_set.all().count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    def __str__(self):
        return self.user.username
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username