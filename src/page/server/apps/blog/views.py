from django.core.paginator import Paginator
from django.http import HttpRequest as HttpRequestBase
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.views.decorators.vary import vary_on_headers
from django_htmx.middleware import HtmxDetails

from page.server.apps.blog.models import Comment, Post


class HttpRequest(HttpRequestBase):
    htmx: HtmxDetails


@vary_on_headers("HX-Request")
def home(request: HttpRequest) -> HttpResponse:
    qs = Post.objects.filter(is_published=True)
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(title__icontains=q)

    page = Paginator(qs, 6).get_page(request.GET.get("page") or 1)
    ctx = {"page": page, "q": q}

    if request.htmx:
        return render(request, "partials/post_list.html", ctx)
    return render(request, "blog/home.html", ctx)


def post_detail(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post.objects.filter(is_published=True), slug=slug)
    comments = post.comments.all()
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments},
    )


@require_http_methods(["POST"])
def add_comment(request: HttpRequest, slug: str) -> HttpResponse:
    post = get_object_or_404(Post, slug=slug, is_published=True)
    name = request.POST.get("author_name", "").strip()
    body = request.POST.get("body", "").strip()
    if name and body:
        Comment.objects.create(post=post, author_name=name, body=body)

    comments = post.comments.all()
    if request.htmx:
        return render(
            request,
            "partials/comment_list.html",
            {"post": post, "comments": comments},
        )
    return render(
        request,
        "blog/post_detail.html",
        {"post": post, "comments": comments},
    )
