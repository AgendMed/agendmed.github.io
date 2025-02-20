from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import ProfissionalSaudeForm, UsuarioForm
from .models import ProfissionalSaude
from AgendaConsulta.models import Consulta
from Campanha.models import Campanha
from Paciente.models import Paciente
from django.http import JsonResponse
from django.shortcuts import render
from .models import ProfissionalSaude


def cadastro_profissional(request):
    if request.method == 'POST':
        usuario_form = UsuarioForm(request.POST)
        profissional_form = ProfissionalSaudeForm(request.POST)

        if usuario_form.is_valid() and profissional_form.is_valid():
            usuario = usuario_form.save()
            profissional = profissional_form.save(commit=False)
            profissional.usuario = usuario
            profissional.save()

            content_type_campanha = ContentType.objects.get_for_model(Campanha)
            content_type_paciente = ContentType.objects.get_for_model(Paciente)
            content_type_consulta = ContentType.objects.get_for_model(Consulta)

            if profissional.especialidade.nome.lower() == 'agente de saúde':
                grupo = Group.objects.get(name='Agente_Saude')
                permissoes = Permission.objects.filter(
                    codename__in=['pode_cadastrar_campanha', 'pode_cadastrar_paciente', 'pode_cadastrar_consulta'],
                    content_type__in=[content_type_campanha, content_type_paciente, content_type_consulta]
                )
            else:
                grupo = Group.objects.get(name='Medico')
                permissoes = Permission.objects.filter(
                    codename__in=['pode_atender', 'pode_visualizar_pacientes'],
                    content_type__in=[content_type_consulta, content_type_paciente]
                )

            profissional.usuario.groups.add(grupo)
            profissional.usuario.user_permissions.add(*permissoes)
            return redirect('sucesso')
    else:
        usuario_form = UsuarioForm()
        profissional_form = ProfissionalSaudeForm()

    return render(request, 'Formularios/cad_profissional.html', {'usuario_form': usuario_form, 'profissional_form': profissional_form})


def sucesso(request):
    return render(request, 'Profissional/sucesso.html')


@login_required
@permission_required('consulta.pode_atender')
def atender_paciente(request):
    return render(request, 'Profissional/atender_paciente.html')


@login_required
def pagina_inicial(request):
    return render(request, 'Profissional/Paginainicial.html')


@login_required
def editar_perfil_profissional(request):
    usuario = request.user
    profissional = get_object_or_404(ProfissionalSaude, usuario=usuario)

    if request.method == 'POST':
        user_form = UsuarioForm(request.POST, instance=usuario)
        profissional_form = ProfissionalSaudeForm(request.POST, instance=profissional)

        if user_form.is_valid() and profissional_form.is_valid():
            user_form.save()
            profissional_form.save()

            nova_senha = profissional_form.cleaned_data.get('nova_senha')
            if nova_senha:
                usuario.set_password(nova_senha)
                usuario.save()
                update_session_auth_hash(request, usuario)

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('profissional:perfil_profissional')
    else:
        user_form = UsuarioForm(instance=usuario)
        profissional_form = ProfissionalSaudeForm(instance=profissional)

    return render(request, 'usuarios/editar_perfil_profissional.html', {'user_form': user_form, 'profissional_form': profissional_form})


@login_required
def perfil_profissional(request):
    profissional = get_object_or_404(ProfissionalSaude, usuario=request.user)
    return render(request, 'usuarios/perfil_profissional.html', {'usuario': request.user, 'profissional': profissional})

def filtrar_profissionais(request):
    unidade_id = request.GET.get('unidade_id')
    if unidade_id:
        profissionais = ProfissionalSaude.objects.filter(unidade_saude_id=unidade_id)
        profissionais_dict = {p.id: str(p) for p in profissionais}
        return JsonResponse(profissionais_dict)
    return JsonResponse({})