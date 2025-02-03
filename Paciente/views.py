<<<<<<< HEAD
#views.py

=======
from django.shortcuts import render, redirect
>>>>>>> ed0684d553c3c83e57c0610639323e0c1eedf970
from .forms import CadastroPacienteForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
<<<<<<< HEAD
from django.contrib.auth.decorators import login_required
from .models import Paciente
from django.contrib.auth import logout as auth_logout  # Renomeando a importação para evitar conflito


def cadastro_paciente(request):
    if request.method == 'POST':
        # Formulário enviado pelo cliente
        form = CadastroPacienteForm(request.POST, request.FILES)  # Captura os dados e arquivos
        if form.is_valid():
            form.save()
            return redirect('Paciente:sucesso')
        else:
            
=======
from django.contrib.auth.models import Group, Permission

def cadastro_paciente(request):
    if request.method == 'POST':
        form = CadastroPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            paciente = form.save() 

            # Adiciona o usuário ao grupo "Paciente"
            grupo_paciente = Group.objects.get(name='Paciente')
            paciente.usuario.groups.add(grupo_paciente)
            permissao_consultar = Permission.objects.get(codename='pode_consultar')
            paciente.usuario.user_permissions.add(permissao_consultar)

            return redirect('Paciente:sucesso')
        else:
>>>>>>> ed0684d553c3c83e57c0610639323e0c1eedf970
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        form = CadastroPacienteForm()
        return render(request, 'usuarios/cadastro.html', {'form': form})

<<<<<<< HEAD
@login_required
def pagina_paciente(request):
    usuario = request.user  # Obtém o usuário logado
    try:
        paciente = Paciente.objects.get(usuario=usuario)  # Obtém o paciente associado ao usuário
    except Paciente.DoesNotExist:
        paciente = None  # Caso não exista, paciente será None

    return render(request, 'usuarios/user.html', {'usuario': usuario, 'paciente': paciente})

=======
>>>>>>> ed0684d553c3c83e57c0610639323e0c1eedf970
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
            return redirect('Paciente:pagina_paciente')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'Login/login.html', {'form': form})
<<<<<<< HEAD

from django.shortcuts import redirect
from .forms import UsuarioForm, PacienteForm  # Supondo que você tenha formulários para Usuario e Paciente

@login_required
def editar_perfil(request):
    usuario = request.user
    try:
        paciente = Paciente.objects.get(usuario=usuario)
    except Paciente.DoesNotExist:
        paciente = None

    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST, instance=usuario)
        paciente_form = PacienteForm(request.POST, instance=paciente)

        if usuario_form.is_valid() and paciente_form.is_valid():
            usuario_form.save()
            paciente_form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('Paciente:pagina_paciente')  # Redireciona para a página do paciente
    else:
        usuario_form = UsuarioForm(instance=usuario)
        paciente_form = PacienteForm(instance=paciente)

    return render(request, 'usuarios/editar_perfil.html', {
        'usuario_form': usuario_form,
        'paciente_form': paciente_form
    })
    
def logout_view(request):
    auth_logout(request)  # Faz o logout do usuário
    return redirect('Paciente:login')  # Redireciona para a página de login
=======
>>>>>>> ed0684d553c3c83e57c0610639323e0c1eedf970
