import re
from django.contrib import messages
from django.contrib.messages import constants
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def valida_senha(request, senha, confirma_senha):
    if len(senha.strip()) == 0 or len(confirma_senha.strip()) == 0:
        messages.add_message(request, messages.ERROR, "senha em branco")
        return False
    
    if len(senha) < 6:
        messages.add_message(request, messages.ERROR, "senha deve ter no minimo 6 caracteres")
        return False
    
    if not senha == confirma_senha:
        messages.add_message(request, messages.ERROR, "senhas não coicidem")
        return False

    if not re.search('[A-Z]', senha):
        messages.add_message(request, messages.ERROR, 'Sua senha não contem letras maiúsculas')
        return False

    if not re.search('[a-z]', senha):
        messages.add_message(request, messages.ERROR, 'Sua senha não contem letras minúsculas')
        return False

    if not re.search('[1-9]', senha):
        messages.add_message(request, messages.ERROR, 'Sua senha não contém números')
        return False
    
    return True

def valida_campo_branco(request, *args):
    for x in args:
        if len(x.strip()) == 0:
            messages.add_message(request, messages.WARNING, 'todos os campos são obrigatorios')
            return False
    return True

def email_html(path_template: str, assunto: str, para: list, **kwargs) -> dict:
    
    html_content = render_to_string(path_template, kwargs)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(assunto, text_content, settings.EMAIL_HOST_USER, para)

    email.attach_alternative(html_content, "text/html")
    email.send()
    return {'status': 1}