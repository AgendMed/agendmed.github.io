#views.py

from django.shortcuts import render, redirect
from .forms import CadastroPacienteForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import Group, Permission

def cadastro_paciente(request):
    if request.method == 'POST':
        # Formulário enviado pelo cliente
        form = CadastroPacienteForm(request.POST, request.FILES)  # Captura os dados e arquivos
        if form.is_valid():
            paciente = form.save()  # Salva o paciente

            # Adiciona o usuário ao grupo "Paciente"
            grupo_paciente = Group.objects.get(name='Paciente')
            paciente.usuario.groups.add(grupo_paciente)  # Associa o paciente ao grupo

            # Opcional: Adiciona permissões específicas ao paciente (se necessário)
            # Aqui você pode adicionar permissões personalizadas se quiser
            # Exemplo: Permissão para consultar
            permissao_consultar = Permission.objects.get(codename='pode_consultar')
            paciente.usuario.user_permissions.add(permissao_consultar)

            # Redireciona para a página de sucesso
            return redirect('Paciente:sucesso')
        else:
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        # Requisição GET: exibe o formulário vazio
        form = CadastroPacienteForm()
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
