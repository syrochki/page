from django.contrib import admin

from page.server.apps.blog.models import Comment, Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin[Post]):
    exclude = ("slug", )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin[Comment]):
    pass


