from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.utils import timezone

from .models import Post
from .post import PostForm


def index(request):
    post = get_list_or_404(Post.objects.filter(
        is_published=True).order_by('-id'))
    return render(request, 'blog/index.html', {'post': post})


def detail(request, pk, slug):
    details = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, 'blog/detail.html', context={'details': details})


def post(request):

    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/post.html', {'form': form})


def edit(request, pk):
    edit = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES, instance=edit)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.created_at = timezone.now()
            edit.save()
            return redirect('blog:index')
    else:
        form = PostForm(instance=edit)

    return render(request, 'blog/post.html', {'form': form})
