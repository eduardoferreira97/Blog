import re

from django.core.exceptions import ValidationError


# Forma 3
def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()


def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)


# Verificação senha com Regex (low case, upper case e numbers)

def strong_password(password):
    # regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')
    regex = re.compile(r'^(?=.*[a-z]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'A senha precisa ter uma letra minúscula. '
            # 'uma letra minúscula e números.'
            # 'Precisa ter no mínimo 8 caracteres.'
        ),
            code='Invalid'
        )


def validate_number(password):
    if not re.findall('\d', password):
        raise ValidationError(
            ("O password precisar conter pelo menos 1 número."),
            code='password_no_len',
        )


def validate_symbol(password):
    if not re.findall('[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
        raise ValidationError(
            ("O password precisar conter pelo menos 1 caracter especial: " +
             "()[]{}|\`~!@#$%^&*_-+=;:'\",<>./?"),
            code='password_no_symbol',
        )


def validate_upper(password):
    if not re.findall('[A-Z]', password):
        raise ValidationError(
            ("O password precisar conter pelo menos 1 letra maiúscula, A-Z."),
            code='password_no_upper',
        )


def validate_len(password):
    if not re.findall('[0-9]', password):
        raise ValidationError(
            ("O password precisar conter pelo menos 8 caracteres."),
            code='password_len',
        )
