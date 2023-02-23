from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.translation import gettext as _

from blog.models import Post

from .forms import LoginForm, RegisterForm
from .tokens import account_activation_token


def activateEmail(request, user, to_email):
    mail_subject = _(f'Ativação de conta - {user.username}')
    message = render_to_string('login/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, _(f'<strong>{user}</strong>, vá por favor para o \
                         seu email: <strong>{to_email}</strong> e click no \
            link recebido para confirmar e completar o seu registro.<br>\
                         <strong>Nota:</strong>\
                          Verifique a sua caixa de spam.'))
    else:
        messages.error(
            request, _(f'problema ao enviar o email de confirmação para \
                {to_email}, verifique se o e-mail foi digitado corretamente.'))


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(
            request, _('Obrigado por confirmar o seu e-mail. Agora você pode\
                  fazer o login na sua conta.'))
        return redirect('login:login')
    else:
        messages.error(request, _('O link de ativação é válido'))

    return redirect('blog:index')


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
        user.is_active = False
        user.save()
        activateEmail(request, user, form.cleaned_data.get('email'))

        del (request.session['register_form_data'])
        return redirect(reverse('login:login'))

    messages.error(request, _('Erro ao criar a conta'))

    return redirect('login:register')


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
            messages.success(request, _('Você está logado'))
            login(request, authenticate_user)
            return redirect(login_url)
        if not request.user.is_active:
            messages.error(
                request, _('Sua conta ainda não foi ativada'))
            return redirect(login_url)
        messages.error(request, _('Credenciais inválidas'))
        return redirect(login_url)
    messages.error(request, _('Erro ao validar os dados'))
    return redirect(login_url)


def login_view(request):
    form = LoginForm()

    detalhe = Post.objects.filter(
        author__id=request.user.id).order_by('-id')

    return render(request, 'login/login.html', {
        'forms': form,
        'detalhe': detalhe,
        'form_action': reverse('login:login_create')
    })


@login_required(login_url='login:login', redirect_field_name='next')
def logout_view(request):

    if not request.POST:
        return redirect(reverse('login:login'))

    if request.POST.get('username') != request.user.username:
        return redirect(reverse('login:login'))

    logout(request)
    return redirect(reverse('login:login'))
