from AgendaConsulta.models import Consulta, Notificacao
from .forms import CadastroPacienteForm
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Paciente
from django.contrib.auth import logout as auth_logout 
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import update_session_auth_hash            
from django.contrib.auth.decorators import login_required
from django.db.models import F
from AgendaConsulta.views import agendar_consulta
from django.contrib.auth import login
from django.http import JsonResponse
import time
from .forms import UsuarioForm, PacienteForm 
from Unidade_Saude.models import UnidadeSaude
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CadastroPacienteForm

def cadastro_paciente(request):
    unidades_saude = UnidadeSaude.objects.all()  # todas as unidades de saúde
    if request.method == 'POST':
        form = CadastroPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                paciente = form.save()
                grupo_paciente = Group.objects.get(name='Paciente')
                paciente.usuario.groups.add(grupo_paciente)
                permissao_consultar = Permission.objects.get(codename='pode_consultar')
                paciente.usuario.user_permissions.add(permissao_consultar)
                messages.success(request, 'Cadastro realizado com sucesso! Você pode fazer login agora.')
                return redirect('Paciente:login')
            except Exception as e:
                messages.error(request, f"Erro ao cadastrar: {str(e)}")
        else:
            print("Erros do formulário:", form.errors)
            messages.error(request, "Por favor, corrija os erros no formulário.")
    else:
        form = CadastroPacienteForm()

    return render(request, 'usuarios/cadastro.html', {
        'form': form,
        'unidades_saude': unidades_saude
    })





@login_required
def pagina_paciente(request):
    usuario = request.user  # Obtém o usuário logado
    try:
        paciente = Paciente.objects.get(usuario=usuario)
    except Paciente.DoesNotExist:
        paciente = None 

    return render(request, 'usuarios/user.html', {'usuario': usuario, 'paciente': paciente})

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
            return redirect('Paciente:paciente_home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")
    else:
        form = AuthenticationForm()
    
    return render(request, 'Login/login.html', {'form': form})



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

            # Verifica se a nova senha foi fornecida
            nova_senha = usuario_form.cleaned_data.get('nova_senha')
            if nova_senha:
                usuario.set_password(nova_senha)
                usuario.save()
                update_session_auth_hash(request, usuario)  # Mantém o usuário logado após a mudança de senha

            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('Paciente:pagina_paciente')  # Redireciona para a página do paciente
    else:
        usuario_form = UsuarioForm(instance=usuario)
        paciente_form = PacienteForm(instance=paciente)

    return render(request, 'usuarios/editar_perfil_paciente.html', {
        'usuario_form': usuario_form,
        'paciente_form': paciente_form
    })
    
def logout_view(request):
    auth_logout(request)  # Faz o logout do usuário
    return redirect('Paciente:login')  # Redireciona para a página de login

# @login_required
# def paciente_home(request):
#     return render(request, 'paciente/home.html', {})

@login_required
def paciente_home(request):
    consultas = Consulta.objects.annotate(
        total_fichas=F('qtd_fichas_prioritarias') + F('qtd_fichas_normais')
    ).filter(total_fichas__gt=0)

    return render(request, 'paciente/home.html', {'consultas': consultas})

@login_required
def agendar_consulta(request):
    return render(request, agendar_consulta)


@login_required
def listar_consultas(request):
    consultas = Consulta.objects.annotate(
        total_fichas=F('qtd_fichas_prioritarias') + F('qtd_fichas_normais')
    ).filter(total_fichas__gt=0)

    return render(request, 'lista_consultas.html', {'consultas': consultas})


@login_required
def notificacoes(request):
    paciente = request.user.paciente_set.first()
    notificacoes = Notificacao.objects.filter(paciente=paciente).order_by('-data_criacao')
    return render(request, 'Paciente/notificacao.html', {'notificacoes': notificacoes})


#marcar se a notificacao foi lida
@login_required
def marcar_como_lida(request, notificacao_id):
    paciente = Paciente.objects.filter(usuario=request.user).first()
    if not paciente:
        return JsonResponse({'success': False, 'message': 'Este usuário não é um paciente.'}, status=403)

    notificacao = get_object_or_404(Notificacao, id=notificacao_id, paciente=paciente)
    
    # Marca a notificação como lida
    notificacao.lida = True
    notificacao.save()

    # Retorna uma resposta JSON para o frontend
    return JsonResponse({'success': True, 'message': 'Notificação marcada como lida.'})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from AgendaConsulta.models import Consulta, Agendamento
from Paciente.models import Paciente

@login_required
def lista_minhas_consultas(request):
    # Obtém o paciente associado ao usuário logado
    paciente = get_object_or_404(Paciente, usuario=request.user)
    
    # Obtém todos os agendamentos do paciente
    agendamentos = Agendamento.objects.filter(paciente=paciente).select_related('consulta')
    
    return render(request, 'paciente/lista_minhas_consultas.html', {'agendamentos': agendamentos})

@login_required
def cancelar_agendamento(request, agendamento_id):
    # Obtém o agendamento que será cancelado
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, paciente__usuario=request.user)
    
    # Obtém a consulta associada ao agendamento
    consulta = agendamento.consulta
    
    # Libera a ficha (prioritária ou normal) de volta para a consulta
    if agendamento.paciente.status == 'prioritario':
        consulta.qtd_fichas_prioritarias += 1
    else:
        consulta.qtd_fichas_normais += 1 
    
    # Salva a consulta atualizada
    consulta.save()
    
    # Deleta o agendamento
    agendamento.delete()
    
    # Exibe uma mensagem de sucesso
    messages.success(request, "Agendamento cancelado com sucesso. A ficha foi liberada para outros pacientes.")
    
    # Redireciona de volta para a lista de agendamentos
    return redirect('Paciente:lista_minhas_consultas')