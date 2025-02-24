from django.contrib import messages
from django.db import transaction
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Consulta, Agendamento, Notificacao
from Paciente.models import Paciente
from Profissional.models import ProfissionalSaude
from .forms import ConsultaForm, AgendamentoForm
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from .models import Consulta
from django.contrib.auth.decorators import login_required, permission_required

@login_required
#@permission_required('AgendaConsulta.pode_cadastrar_consulta', raise_exception=True)
def cadastrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta cadastrada com sucesso!")
            return redirect('AgendaConsulta:listar_consultas')
        else:
            messages.error(request, "Erro ao cadastrar. Verifique os dados.")
    else:
        form = ConsultaForm()
    
    return render(request, 'Formularios/cad_Consulta.html', {'form': form})




@login_required
def agendar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    usuario = request.user
    paciente = get_object_or_404(Paciente, usuario=usuario)

    tipo_ficha_padrao = 'prioritario' if paciente.status == 'prioritario' else 'comum'

    # Obtém a última posição para cada fila
    ultima_posicao_prioritaria = (
        Agendamento.objects.filter(consulta=consulta, paciente__status='prioritario')
        .order_by('-numero_na_fila')
        .values_list('numero_na_fila', flat=True)
        .first()
    ) or 0

    ultima_posicao_comum = (
        Agendamento.objects.filter(consulta=consulta, paciente__status='comum')
        .order_by('-numero_na_fila')
        .values_list('numero_na_fila', flat=True)
        .first()
    ) or 0

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tipo_ficha = form.cleaned_data.get('tipo_ficha', tipo_ficha_padrao)

                    if tipo_ficha == 'prioritario':
                        if consulta.qtd_fichas_prioritarias > 0:
                            numero_na_fila = ultima_posicao_prioritaria + 1
                            consulta.qtd_fichas_prioritarias -= 1
                        else:
                            consulta.lista_espera_prioritaria.add(paciente)
                            messages.warning(request, "Todas as fichas prioritárias foram distribuídas. Você foi adicionado à fila de espera.")
                            return redirect('Paciente:paciente_home')

                    else:
                        if consulta.qtd_fichas_normais > 0:
                            numero_na_fila = ultima_posicao_comum + 1
                            consulta.qtd_fichas_normais -= 1
                        else:
                            consulta.lista_espera_comum.add(paciente)
                            messages.warning(request, "Todas as fichas normais foram distribuídas. Você foi adicionado à fila de espera.")
                            return redirect('Paciente:paciente_home')

                    consulta.save()

                    agendamento = form.save(commit=False)
                    agendamento.consulta = consulta
                    agendamento.paciente = paciente
                    agendamento.numero_na_fila = numero_na_fila
                    agendamento.save()

                    messages.success(request, f'Agendamento realizado com sucesso! Você é o número {numero_na_fila} na fila de {tipo_ficha}.')
                    return redirect('Paciente:paciente_home')

            except Exception as e:
                messages.error(request, str(e))
                return redirect('AgendaConsulta:agendar_consulta', consulta_id=consulta_id)
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = AgendamentoForm(initial={'consulta': consulta, 'tipo_ficha': tipo_ficha_padrao})

    return render(request, 'Paciente/AgendarConsulta.html', {
        'form': form,
        'consulta': consulta,
        'paciente': paciente
    })






# Ainda em testes
def chamar_proximo_paciente(consulta):
    """
    Move um paciente da lista de espera para o agendamento, se houver fichas disponíveis.
    """
    if consulta.qtd_fichas_prioritarias > 0 and consulta.lista_espera_prioritaria.exists():
        # Chamar o primeiro paciente da fila prioritária
        paciente = consulta.lista_espera_prioritaria.first()
        consulta.lista_espera_prioritaria.remove(paciente)
        consulta.qtd_fichas_prioritarias -= 1

    elif consulta.qtd_fichas_normais > 0 and consulta.lista_espera_comum.exists():
        # Chamar o primeiro paciente da fila comum
        paciente = consulta.lista_espera_comum.first()
        consulta.lista_espera_comum.remove(paciente)
        consulta.qtd_fichas_normais -= 1

    else:
        return

    # Criar um novo agendamento para o paciente chamado
    numero_na_fila = Agendamento.objects.filter(consulta=consulta).count() + 1
    Agendamento.objects.create(
        consulta=consulta,
        paciente=paciente,
        numero_na_fila=numero_na_fila
    )

    consulta.save()
    Notificacao.objects.create(
        paciente=paciente,
        mensagem=f"Sua consulta foi confirmada para {consulta.data} às {consulta.horario_inicio}."
    )








#teste de listar consultas (incompleta)
@login_required
def listar_consultas(request):
    profissional = ProfissionalSaude.objects.filter(usuario=request.user).first()
    
    if not profissional:
        messages.error(request, "Este usuário não está cadastrado como profissional de saúde.")
        return redirect('home')

    consultas = Consulta.objects.filter(unidade_saude=profissional.unidade_saude).annotate(
        total_fichas=F('qtd_fichas_prioritarias') + F('qtd_fichas_normais')
    ).filter(total_fichas__gt=0)

    return render(request, 'lista_consultas.html', {'consultas': consultas})



@login_required
def cancelar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    profissional = ProfissionalSaude.objects.filter(usuario=request.user).first()

    if not profissional:
        messages.error(request, "Apenas profissionais de saúde podem cancelar consultas.")
        return redirect('AgendaConsulta:listar_consultas')

    if consulta.unidade_saude != profissional.unidade_saude:
        messages.error(request, "Você não tem permissão para cancelar esta consulta.")
        return redirect('AgendaConsulta:listar_consultas')

    if request.method == 'POST':
        razao = request.POST.get('razao')

        # Notificar e remover todos os pacientes agendados
        agendamentos = Agendamento.objects.filter(consulta=consulta)
        if agendamentos.exists():
            for agendamento in agendamentos:
                Notificacao.objects.create(
                    paciente=agendamento.paciente,
                    mensagem=f"Sua consulta agendada para {consulta.data} foi cancelada. Motivo: {razao}."
                )
                agendamento.delete()

        # Liberar fichas para novas consultas
        consulta.qtd_fichas_prioritarias += len(consulta.lista_espera_prioritaria.all())
        consulta.qtd_fichas_normais += len(consulta.lista_espera_comum.all())

        # Atualizar lista de espera
        consulta.lista_espera_prioritaria.clear()
        consulta.lista_espera_comum.clear()
        
        consulta.save()

        messages.success(request, "Consulta cancelada com sucesso. Os pacientes foram notificados.")
        return redirect('AgendaConsulta:listar_consultas')
    
    return render(request, 'AgendaConsulta/cancelar_consulta.html', {
        'consulta': consulta,
        'profissional': profissional,
    })






@login_required
def editar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == 'POST':
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta editada com sucesso!")
            return redirect('AgendaConsulta:listar_consultas')
        else:
            messages.error(request, "Erro ao editar. Verifique os dados.")
    else:
        form = ConsultaForm(instance=consulta)

    return render(request, 'Formularios/edit_Consulta.html', {'form': form, 'consulta': consulta})



@login_required
def listar_pacientes_por_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    profissional = ProfissionalSaude.objects.filter(usuario=request.user).first()

    if not profissional or consulta.unidade_saude != profissional.unidade_saude:
        messages.error(request, "Você não tem permissão para visualizar esta consulta.")
        return redirect('AgendaConsulta:listar_consultas')

    agendamentos = Agendamento.objects.filter(consulta=consulta).select_related('paciente')

    return render(request, 'profissional/lista_paciente_por_consulta.html', {
        'consulta': consulta,
        'agendamentos': agendamentos
    })