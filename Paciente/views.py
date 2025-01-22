#views.py
<<<<<<< HEAD
from rest_framework.permissions import AllowAny
from Paciente.forms import PacienteForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PacienteSerializer
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import PacienteForm
from .models import Paciente

def cadastro_paciente(request):
    if request.method == 'POST':
        print(request.POST)  # Verifica os dados que estão sendo enviados no POST
        print(request.FILES)  # Verifica os arquivos (caso existam)
        
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            # Hash a senha antes de salvar
            form.cleaned_data['senha'] = make_password(form.cleaned_data['senha'])
            print(form.cleaned_data)  # Imprime os dados limpos do formulário
            form.save()
            return redirect('Paciente:sucesso')
        else:
            print(form.errors)  # Exibe os erros de validação, caso existam
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        form = PacienteForm()
=======

from django.shortcuts import render, redirect
from django.shortcuts import render, redirect
from .forms import CadastroPacienteForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def cadastro_paciente(request):
    if request.method == 'POST':
        # Formulário enviado pelo cliente
        form = CadastroPacienteForm(request.POST, request.FILES)  # Captura os dados e arquivos
        if form.is_valid():  # Valida o formulário
            form.save()  # Salva os dados no banco de dados
            return redirect('template/sucesso.html')  # Redireciona para a página de sucesso
        else:
            # Formulário inválido, renderiza com os erros
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        # Requisição GET: exibe o formulário vazio
        form = CadastroPacienteForm()
>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
        return render(request, 'usuarios/cadastro.html', {'form': form})


def sucesso(request):
<<<<<<< HEAD
    return render(request, 'sucesso.html')  # Renderiza a página de sucesso

def login_view(request):
    if request.method == 'POST':
        cpf = request.POST.get('cpf')
        senha = request.POST.get('senha')

        try:
            usuario = Paciente.objects.get(cpf=cpf)
            # Verifica a senha usando o hash
            if check_password(senha, usuario.senha):
                login(request, usuario)  # Você pode precisar de um User model para isso
                return redirect('Paciente:sucesso')  # Redirecionar para uma página de sucesso
            else:
                return render(request, 'usuarios/login.html', {'error': 'CPF ou senha inválidos.'})
        except Paciente.DoesNotExist:
            return render(request, 'usuarios/login.html', {'error': 'CPF ou senha inválidos.'})

    return render(request, 'usuarios/login.html')
=======
    return render(request, 'sucesso.html')

def Index_view(request):
    return render(request, 'Login/index.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('Paciente:sucesso')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'Login/login.html', {'form': form})

>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
