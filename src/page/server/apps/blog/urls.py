from django.urls import path

from page.server.apps.blog import views

app_name = "blog"

urlpatterns = [
    path("", views.home, name="home"),
    path("posts/<slug:slug>/", views.post_detail, name="post_detail"),
    path("posts/<slug:slug>/comments/", views.add_comment, name="add_comment"),
]
