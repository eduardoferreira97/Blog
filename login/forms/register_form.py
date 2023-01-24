from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from utils.django_forms import (add_placeholder, strong_password, validate_len,
                                validate_number, validate_symbol,
                                validate_upper)


class RegisterForm(forms.ModelForm):

    # Forma 3
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu usuário')
        add_placeholder(self.fields['email'], 'Ex.: email@gmail.com')
        add_placeholder(self.fields['first_name'], 'Ex.: João')
        add_placeholder(self.fields['last_name'], 'Ex.: Alves')

    # Forma 2
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Digite a sua senha'}),
        error_messages={'required': 'Senha não pode ser vazia'},
        # help_text=('A senha precisa ter uma letra maiúscula, '
        #            'uma letra minúscula e números.'
        #            'Precisa ter no mínimo 8 caracteres'),
        validators=[validate_upper, validate_symbol,
                    validate_number, strong_password, validate_len]
    )

    confirm_password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Confirme a sua senha'}),
        error_messages={'required': 'Senha não pode ser vazia'}
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password',]

        labels = {
            'username': 'Usuário',
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'password': 'Senha',
            'confirm_password': 'Confirmar senha',
        }

    # validação do campo, caso ele entre na condição, ele envia um alerta
    def clean_password(self):

        data = self.cleaned_data.get('password')

        if 'aten' in data:
            raise ValidationError(
                'Não digite %(value)s no campo',
                code='Invalid',
                params={'value': '"aten"'}
            )

        return data

    # Verificação para ver se os password são iguais
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise ValidationError({
                'password': 'As senhas precisam se iguais',
                'confirm_password': 'As senhas precisam se iguais'
            })

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            raise ValidationError(
                'O e-mail informado já está em uso. Tente outro')

        return email
