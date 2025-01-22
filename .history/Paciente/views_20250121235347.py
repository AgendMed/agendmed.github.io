#views.py

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
            form.save()
            return redirect('template/sucesso.html') 
            
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        # Requisição GET: exibe o formulário vazio
        form = CadastroPacienteForm()
        return render(request, 'usuarios/cadastro.html', {'form': form})


def sucesso(request):
    return render(request, 'templates/sucesso.html')

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

