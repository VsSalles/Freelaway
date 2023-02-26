from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from . utils import valida_senha, valida_campo_branco, email_html
from django.contrib import messages
from hashlib import sha256
from . models import Ativacao
from django.conf import settings
import os
from django.contrib import auth


def cadastro(request):
    if request.user.is_authenticated:
        return redirect('/jobs/encontrar_jobs')
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('password')
        confirm_senha = request.POST.get('confirm-password')

        if not valida_campo_branco(request, username, email, senha, confirm_senha):
            return redirect('/auth/cadastro')

        if len(username) <3:
            messages.add_message(request,messages.WARNING,'usuario deve ter no minimo 3 letras')
            return redirect('/auth/cadastro')

        if not valida_senha(request, senha, confirm_senha):
            return redirect('/auth/cadastro')
        
        token = sha256(f'{username}{email}'.encode()).hexdigest()
        

        try:
            usuario = User.objects.create_user(username=username, email=email, password=senha, is_active=False)
            usuario.save()
            ativa = Ativacao(token=token, user=usuario)
            ativa.save()
            path_template = os.path.join(settings.BASE_DIR, 'autenticacao/templates/emails/cadastro_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=usuario, link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")
            messages.add_message(request, messages.SUCCESS, 'Usuario cadastrado com sucesso, verifique seu email para ativar sua conta')
            return redirect('/auth/login')
        except Exception as e:
            print(e)
            messages.add_message(request, messages.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')

def login(request):
    if request.user.is_authenticated:
        return redirect('/jobs/encontrar_jobs')
    if request.method == 'GET':
        return render(request, 'login.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')

        if not valida_campo_branco(request,username,senha):
            return redirect('/auth/login')
        
        user = auth.authenticate(username=username, password=senha)

        if not user:
            messages.add_message(request, messages.ERROR, 'Usuario ou senha invalida')
            return redirect('/auth/login')
        else:
            auth.login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Usuario logado com sucesso')
            return redirect('/jobs/encontrar_jobs')

def ativar_conta(request, token):
    if request.user.is_authenticated:
        return redirect('/jobs/encontrar_jobs')
    token = get_object_or_404(Ativacao, token=token)
    if token.ativo:
        messages.add_message(request, messages.WARNING, 'Essa token já foi usado')
        return redirect('/auth/login')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, messages.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/login')

def sair(request):
    auth.logout(request)
    return redirect('/auth/login')
