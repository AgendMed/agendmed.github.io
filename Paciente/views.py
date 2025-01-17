#views.py

from django.shortcuts import render, redirect
from rest_framework.permissions import AllowAny
from Paciente.forms import PacienteForm
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import PacienteSerializer

from django.shortcuts import render, redirect
from .forms import PacienteForm
from .models import Paciente
def cadastro_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Paciente:sucesso')  # Redireciona após o sucesso do cadastro
        else:
            # Aqui você pode tratar os erros de validação e renderizar o formulário com os erros
            return render(request, 'usuarios/cadastro.html', {'form': form})

    form = PacienteForm()  # Cria uma instância vazia do formulário
    return render(request, 'usuarios/cadastro.html', {'form': form})  # Passa o formulário vazio para o template

def sucesso(request):
    return render(request, 'sucesso.html')  # Renderiza a página de sucesso

def login_view(request):
    return render(request, 'Login/login.html')
