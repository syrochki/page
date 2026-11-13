import textwrap
from typing import Any, final, override

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django_stubs_ext.db.models.manager import ManyRelatedManager
from unidecode import unidecode


@final
class Post(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    excerpt = models.TextField(blank=True)
    body = models.TextField()
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    comments: ManyRelatedManager[Comment]

    class Meta:
        ordering = ["-created_at"]

    @override
    def save(self, *args: int, **kwargs: Any) -> None:
        if not self.slug:
            base = slugify(unidecode(self.title)) or "post"
            slug = base
            i = 1
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    @override
    def __str__(self) -> str:
        return textwrap.wrap(self.title, 100 // 4)[0]


@final
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author_name = models.CharField(max_length=80)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    @override
    def __str__(self) -> str:
        return textwrap.wrap(str(self.post), 100 // 4)[0]
