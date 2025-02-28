from django.contrib import messages
from django.db import transaction
from Paciente.models import Paciente
from Profissional.models import ProfissionalSaude
from .forms import ConsultaForm, AgendamentoForm
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from .models import Consulta
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Consulta, Agendamento, Notificacao



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

    # Verifica se o paciente já tem um agendamento nessa consulta
    ja_agendado = Agendamento.objects.filter(consulta=consulta, paciente=paciente).exists()

    numero_na_fila = Agendamento.objects.filter(consulta=consulta).count() + 1

    if request.method == 'POST' and not ja_agendado:
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tipo_ficha = form.cleaned_data.get('tipo_ficha')

                    if tipo_ficha == 'prioritario' and consulta.qtd_fichas_prioritarias < 1:
                        raise ValueError("Não há fichas prioritárias disponíveis")
                    elif tipo_ficha == 'comum' and consulta.qtd_fichas_normais < 1:
                        raise ValueError("Não há fichas normais disponíveis")

                    # Atualiza a quantidade de fichas disponíveis
                    if tipo_ficha == 'prioritario':
                        consulta.qtd_fichas_prioritarias -= 1
                    else:
                        consulta.qtd_fichas_normais -= 1

                    consulta.save()

                    # Salva o agendamento
                    agendamento = form.save(commit=False)
                    agendamento.consulta = consulta
                    agendamento.paciente = paciente
                    agendamento.numero_na_fila = numero_na_fila
                    agendamento.save()

                    messages.success(request, f'Agendamento confirmado! Você é o número {numero_na_fila} na fila.')
                    return render(request, 'Paciente/AgendarConsulta.html', {
                        'form': form, 
                        'consulta': consulta,
                        'numero_na_fila': numero_na_fila,
                        'paciente': paciente,
                        'ja_agendado': ja_agendado
                    })

            except Exception as e:
                messages.error(request, str(e))
    
    else:
        form = AgendamentoForm(initial={'consulta': consulta})
    
    return render(request, 'Paciente/AgendarConsulta.html', {
        'form': form, 
        'consulta': consulta,
        'numero_na_fila': numero_na_fila,
        'paciente': paciente,
        'ja_agendado': ja_agendado
    })



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

    # Verifica se a consulta pertence à unidade de saúde do profissional
    if consulta.unidade_saude != profissional.unidade_saude:
        messages.error(request, "Você não tem permissão para cancelar esta consulta.")
        return redirect('AgendaConsulta:listar_consultas')

    if request.method == 'POST':
        razao = request.POST.get('razao')
        
        # Notifica todos os pacientes agendados para esta consulta
        agendamentos = Agendamento.objects.filter(consulta=consulta)
        if agendamentos.exists():
            for agendamento in agendamentos:
                Notificacao.objects.create(
                    paciente=agendamento.paciente,
                    mensagem=f"Sua consulta agendada para {consulta.data} às {consulta.horario_inicio} foi cancelada. Motivo: {razao}."
                )
                agendamento.delete()
        
        consulta.delete()

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
    
    # Obtém todos os agendamentos para a consulta
    agendamentos = Agendamento.objects.filter(consulta=consulta).select_related('paciente')

    if not agendamentos:
        messages.info(request, "Nenhum paciente agendado para esta consulta.")

    return render(request, 'Profissional/lista_paciente_por_consulta.html', {
        'consulta': consulta,
        'agendamentos': agendamentos
    })



@login_required
def alocar_paciente(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    
    # Acessa o ProfissionalSaude relacionado ao usuário
    try:
        profissional = request.user.profissionalsaude_set.first()
    except AttributeError:
        messages.error(request, "Este usuário não está associado a um profissional de saúde.")
        return redirect('home')

    if not profissional:
        messages.error(request, "Este usuário não está associado a um profissional de saúde.")
        return redirect('home')

    # Obtém as consultas disponíveis na unidade de saúde do profissional
    consultas_disponiveis = Consulta.objects.filter(
        unidade_saude=profissional.unidade_saude,
        qtd_fichas_normais__gt=0
    )

    if request.method == 'POST':
        consulta_id = request.POST.get('consulta_id')
        consulta = get_object_or_404(Consulta, id=consulta_id)

        if Agendamento.objects.filter(consulta=consulta, paciente=paciente).exists():
            messages.error(request, "Este paciente já está agendado para esta consulta.")
            return redirect('AgendaConsulta:alocar_paciente', paciente_id=paciente.id)

        # Verifica se há fichas disponíveis
        if consulta.qtd_fichas_normais < 1:
            messages.error(request, "Não há fichas disponíveis para esta consulta.")
            return redirect('AgendaConsulta:alocar_paciente', paciente_id=paciente.id)

        try:
            with transaction.atomic():
                agendamento = Agendamento(
                    consulta=consulta,
                    paciente=paciente,
                    numero_na_fila=Agendamento.objects.filter(consulta=consulta).count() + 1
                )
                agendamento.save()

                consulta.qtd_fichas_normais -= 1
                consulta.save()

                # Cria a notificação para o paciente
                Notificacao.objects.create(
                    paciente=paciente,
                    mensagem=f"Você foi alocado para a consulta de {consulta.data} às {consulta.horario_inicio}. Você é o número {agendamento.numero_na_fila} na fila."
                )

                messages.success(request, f"Paciente alocado com sucesso na consulta de {consulta.data} às {consulta.horario_inicio}.")
                return redirect('AgendaConsulta:listar_consultas')
        except Exception as e:
            messages.error(request, f"Erro ao alocar paciente: {str(e)}")
            return redirect('AgendaConsulta:alocar_paciente', paciente_id=paciente.id)

    return render(request, 'Profissional/alocar_paciente.html', {
        'paciente': paciente,
        'consultas_disponiveis': consultas_disponiveis
    })