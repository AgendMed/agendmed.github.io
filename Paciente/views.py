from .forms import CadastroPacienteForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import login_required



def cadastro_paciente(request):
    if request.method == 'POST':
        form = CadastroPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            paciente = form.save() 

            grupo_paciente = Group.objects.get(name='Paciente')
            paciente.usuario.groups.add(grupo_paciente)
            permissao_consultar = Permission.objects.get(codename='pode_consultar')
            paciente.usuario.user_permissions.add(permissao_consultar)

            return redirect('Paciente:sucesso')
        else:
            return render(request, 'usuarios/cadastro.html', {'form': form})
    else:
        form = CadastroPacienteForm()
        return render(request, 'usuarios/cadastro.html', {'form': form})

def sucesso(request):
    return render(request, 'sucesso.html')

def Index_view(request):
    return render(request, 'Login/index.html')


@login_required
def agendar_consulta(request):
    return render(request, 'Paciente/AgendarConsulta.html')