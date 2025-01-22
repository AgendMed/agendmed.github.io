#views.py

from django.shortcuts import render, redirect
from Paciente.forms import PacienteForm
from django.shortcuts import render, redirect
from .forms import CadastroPacienteForm, PacienteForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages

def cadastro_paciente(request):
    if request.method == 'POST':
        print(request.POST)
        print(request.FILES)  
        
        form = CadastroPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            print(form.cleaned_data)  # Imprime os dados limpos do formulário
            form.save()
            return redirect('Paciente:sucesso')
        else:
            print(form.errors)
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        form = PacienteForm()
        return render(request, 'usuarios/cadastro.html', {'form': form})


def sucesso(request):
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

