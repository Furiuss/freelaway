from contextlib import redirect_stdout
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

def cadastro(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('encontrar_jobs')
        return render(request, 'cadastro.html')
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm-password')
        
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não coincidem')
            return redirect('cadastro')
        
        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Username & Senhas não podem ser vazios')
            return redirect('cadastro')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.add_message(request, constants.ERROR, 'Esse usuário já existe')
            return redirect('cadastro')

        try:
            user = User.objects.create_user(username=username, password=senha)
            user.save()

            return redirect('logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('cadastro')


def logar(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('encontrar_jobs')
        return render(request, 'login.html')
        
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')
        
        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Username & Senhas não podem ser vazios')
            return redirect('logar')
        
        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('logar')
        else:
            auth.login(request, usuario)
            return redirect('encontrar_jobs')                


def sair(request):
    auth.logout(request)
    return redirect('logar')
