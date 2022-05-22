from random import choices
from django import forms
from.models import Category, Post, Comment

class PostForm(forms.ModelForm):
    status = forms.CharField(choices = Post.OPTIONS)
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(), empty_label="Select")
    class Meta:
        model = Post
        fields = (
            "title",
            "image",
            "content",
            "category",
            "status",
        )

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("content")