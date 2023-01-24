from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse

from .forms import LoginForm, RegisterForm


def register_view(request):
    register_form_data = request.session.get('register_form_data', None)
    forms = RegisterForm(register_form_data)
    return render(request, "login/register_user.html", {
        'forms': forms,
        'form_action': reverse('login:register_create')})


def register_create(request):
    if not request.POST:
        raise Http404()

    POST = request.POST
    request.session['register_form_data'] = POST
    form = RegisterForm(POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'Sua conta foi criada, faça login')

        del (request.session['register_form_data'])
        return redirect(reverse('login:login'))

    messages.error(request, 'Erro ao criar a conta')

    return redirect('login:register')


def login_view(request):
    form = LoginForm()
    return render(request, 'login/login.html', {
        'forms': form,
        'form_action': reverse('login:login_create')
    })


def login_create(request):

    if not request.POST:
        raise Http404()

    form = LoginForm(request.POST)
    login_url = reverse('login:login')

    if form.is_valid():

        authenticate_user = authenticate(

            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )

        if authenticate_user is not None:
            messages.success(request, 'Você está logado')
            login(request, authenticate_user)
            return redirect(login_url)
        messages.error(request, 'Credenciais inválidas')
        return redirect(login_url)
    messages.error(request, 'Erro ao validar os dados')
    return redirect(login_url)


@login_required(login_url='login:login', redirect_field_name='next')
def logout_view(request):

    if not request.POST:
        return redirect(reverse('login:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('login:login'))

    logout(request)
    return redirect(reverse('blog:index'))
