from django.urls import path
from .views import post_delete, post_detail, post_list, post_create, post_update, like
app_name = "blogapp"
urlpatterns = [
    path("", post_list, name="list" ),
    path("create", post_create, name="create" ),
    path("<str:slug>/", post_detail, name="detail" ),
    path("<str:slug>/update", post_update, name="update" ),
    path("<str:slug>/delete", post_delete, name="delete" ),
    path("<str:slug>/like/",like, name="like"),
]

