from email.policy import default
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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)