from django.shortcuts import render, redirect
from .forms import ProfissionalSaudeForm
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import permission_required
from django.contrib.contenttypes.models import ContentType
from AgendaConsulta.models import Consulta
from Campanha.models import Campanha
from Paciente.models import Paciente
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def cadastro_profissional(request):
    if request.method == 'POST':
        form = ProfissionalSaudeForm(request.POST)
        if form.is_valid():
            profissional = form.save()

            content_type_campanha = ContentType.objects.get_for_model(Campanha)
            content_type_paciente = ContentType.objects.get_for_model(Paciente)
            content_type_consulta = ContentType.objects.get_for_model(Consulta)

            especialidade = profissional.especialidade.nome.lower()

            if especialidade == 'agente de saúde':
                grupo_agente_saude = Group.objects.get(name='Agente_Saude')
                profissional.usuario.groups.add(grupo_agente_saude)
                
                permissao_cadastrar_campanha = Permission.objects.get(
                    codename='pode_cadastrar_campanha',
                    content_type=content_type_campanha
                )
                permissao_cadastrar_paciente = Permission.objects.get(
                    codename='pode_cadastrar_paciente',
                    content_type=content_type_paciente
                )
                permissao_cadastrar_consulta = Permission.objects.get(
                    codename='pode_cadastrar_consulta',
                    content_type=content_type_consulta
                )
                profissional.usuario.user_permissions.add(
                    permissao_cadastrar_campanha,
                    permissao_cadastrar_paciente,
                    permissao_cadastrar_consulta
                )
            
            else:
                grupo_medico = Group.objects.get(name='Medico')
                profissional.usuario.groups.add(grupo_medico)
                
                permissao_atender = Permission.objects.get(
                    codename='pode_atender',
                    content_type=content_type_consulta
                )
                permissao_visualizar = Permission.objects.get(
                    codename='pode_visualizar_pacientes',
                    content_type=content_type_paciente
                )
                profissional.usuario.user_permissions.add(
                    permissao_atender,
                    permissao_visualizar
                )
            
            return redirect('sucesso')
    else:
        form = ProfissionalSaudeForm()

    return render(request, 'Formularios/cad_profissional.html', {'form': form})

def sucesso(request):
    return render(request, 'Profissional/sucesso.html')


@permission_required('consulta.pode_atender')
def atender_paciente(request):
    return None



@permission_required('consulta.pode_atender')
def atender_paciente(request):
    return None


# def profissional_home(request):
#     return render(request, 'profissional/profissional_home.html')
@login_required
def pagina_inicial(request):
    return render(request, 'Profissional/Paginainicial.html')




'''
@login_required
def editar_perfil(request):
    if request.method == 'POST':
        form = EditarPerfilForm(request.POST, instance=request.user)
        if form.is_valid():
            # Garante que o CPF não será alterado
            instance = form.save(commit=False)
            instance.cpf = request.user.cpf  # Mantém o CPF original
            instance.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('profissional:paginainicial')
    else:
        form = EditarPerfilForm(instance=request.user)
    
    return render(request, 'Profissional/editar_perfil.html', {'form': form})

'''''
