from django.contrib import messages
from django.contrib.auth import get_user
from django.contrib.auth.decorators import login_required
from django.core.mail import BadHeaderError, send_mail
# PERMITE USAR A CONDICIONAL 'OR' NO FILTRO DO BANCO DE DADOS
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import (get_list_or_404, get_object_or_404, redirect,
                              render)
from django.utils import timezone

from .forms import ContactForm, PostForm
from .models import Post


def contato(request):

    if request.method == "GET":
        form = ContactForm()
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data["subject"]
            from_email = form.cleaned_data["email"]
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email,
                          ["projetodjango23@gmail.com"])
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return redirect('blog:contato')
    return render(request, "blog/contact.html", {"form": form})


def index(request):
    post = Post.objects.filter(
        is_published=True).order_by('-id')

    return render(request, 'blog/index.html', {'post': post,
                                               'title': 'Home'})


def search(request):

    search = request.GET.get('search')

    result = Post.objects.filter(
        Q(title__contains=search) | Q(sub_title__contains=search)
        | Q(author__username__contains=search) | Q(text__contains=search)
    ).order_by('-id')

    return render(request, 'blog/search_result.html',
                  {'result': result,
                   'search': search,
                   'title': f'Pesquisa: {search}'})


def detail(request, pk, slug):
    details = get_object_or_404(Post, pk=pk, is_published=True)
    return render(request, 'blog/detail.html', {'details': details,
                                                'title': f'{details.title}'})


def post(request):

    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_at = timezone.now()
            post.author = get_user(request)
            post.save()
            return redirect('blog:index')
    else:
        form = PostForm()
    return render(request, 'blog/post.html', {'form': form})


@login_required
def edit(request, pk):
    edit = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES, instance=edit)
        if form.is_valid():
            edit = form.save(commit=False)
            edit.update_at = timezone.now()
            edit.author = get_user(request)
            edit.save()
            return redirect('blog:index')
    else:
        form = PostForm(instance=edit)

    return render(request, 'blog/post.html', {'form': form})


@login_required
def delete(request, pk):
    form = get_object_or_404(Post, pk=pk)
    titulo = form.title
    form.delete()
    messages.success(
        request,  f'Post <strong>{titulo}</strong> foi deletado com sucesso.')
    return redirect('blog:index')


def filter(request, pk, username):
    filter = get_list_or_404(Post.objects.filter(
        author__id=pk).order_by('-id'))
    return render(request, 'blog/index.html', {'post': filter,
                                               'title': f'{username} | Posts'})
