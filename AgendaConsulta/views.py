from django.contrib import messages
from django.db import transaction
from .forms import ConsultaForm, AgendamentoForm
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from .models import Consulta
from django.contrib.auth.decorators import login_required, permission_required

@login_required
@permission_required('AgendaConsulta.pode_cadastrar_consulta', raise_exception=True)
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


def agendar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    paciente = form.cleaned_data['paciente']
                    
                    if paciente.status == 'prioritario':
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
                    agendamento.save()
                    
                    messages.success(request, 'Agendamento realizado com sucesso!')
                    return redirect('listar_consultas')
            
            except Exception as e:
                messages.error(request, str(e))
                return redirect('agendar_consulta', consulta_id=consulta_id)
        else:
            messages.error(request, 'Por favor corrija os erros no formulário')
    else:
        form = AgendamentoForm(initial={'consulta': consulta})
    
    return render(request, 'Paciente/AgendarConsulta.html', {'form': form, 'consulta': consulta})




#teste de listar consultas (incompleta)
def listar_consultas(request):
    consultas = Consulta.objects.annotate(
        total_fichas=F('qtd_fichas_prioritarias') + F('qtd_fichas_normais')
    ).filter(total_fichas__gt=0)

    return render(request, 'lista_consultas.html', {'consultas': consultas})





from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Consulta, Agendamento, Notificacao  # Importe o modelo Notificacao

@login_required
def cancelar_consulta(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)

    if request.method == 'POST':
        razao = request.POST.get('razao')

        # Obter todos os agendamentos para esta consulta
        agendamentos = Agendamento.objects.filter(consulta=consulta)

        if agendamentos.exists():
            for agendamento in agendamentos:
                # Criar uma notificação para o paciente
                Notificacao.objects.create(
                    paciente=agendamento.paciente,
                    mensagem=f"Sua consulta na unidade de saúde {consulta.unidade_saude.nome} foi cancelada. Razão: {razao}."
                )

            # Marcar a consulta como cancelada (ou excluí-la)
            consulta.delete()  # Ou você pode adicionar um campo `cancelada` no modelo Consulta e marcá-la como True

            messages.success(request, 'Consulta cancelada com sucesso e notificações enviadas aos pacientes.')
        else:
            messages.error(request, 'Nenhum agendamento encontrado para esta consulta.')
        
        return redirect('AgendaConsulta:listar_consultas')

    return redirect('AgendaConsulta:listar_consultas')