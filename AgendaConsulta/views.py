from django.contrib import messages
from django.db import transaction

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

    # Definir o tipo de ficha automaticamente com o status do paciente
    tipo_ficha_padrao = 'prioritario' if paciente.status == 'prioritario' else 'comum'
    
    # Contar quantos pacientes já estão na fila
    numero_na_fila = Agendamento.objects.filter(consulta=consulta).count() + 1

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    tipo_ficha = form.cleaned_data.get('tipo_ficha', tipo_ficha_padrao)

                    if tipo_ficha == 'prioritario':
                        if consulta.qtd_fichas_prioritarias < 1:
                            raise ValueError("Não há fichas prioritárias disponíveis")
                        consulta.qtd_fichas_prioritarias -= 1
                    else:
                        if consulta.qtd_fichas_normais < 1:
                            raise ValueError("Não há fichas normais disponíveis")
                        consulta.qtd_fichas_normais -= 1

                    consulta.save()
                    
                    agendamento = form.save(commit=False)
                    agendamento.consulta = consulta
                    agendamento.paciente = paciente
                    agendamento.numero_na_fila = numero_na_fila
                    agendamento.save()

                    messages.success(request, f'Agendamento disponível! Você é o número {numero_na_fila} na fila.')
                    return redirect('Paciente:paciente_home')
            
            except Exception as e:
                messages.error(request, str(e))
                return redirect('AgendaConsulta:agendar_consulta', consulta_id=consulta_id)
        else:
            messages.error(request, 'Por favor corrija os erros no formulário')
    else:
        form = AgendamentoForm(initial={'consulta': consulta, 'tipo_ficha': tipo_ficha_padrao})
    
    return render(request, 'Paciente/AgendarConsulta.html', { ######################
        'form': form, 
        'consulta': consulta,
        'numero_na_fila': numero_na_fila,
        'paciente': paciente 
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







from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Consulta, Agendamento, Notificacao

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
        
        # Deleta a consulta
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
