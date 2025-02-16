from django.contrib import messages
from django.db import transaction
from .forms import ConsultaForm, AgendamentoForm
from django.db.models import F
from django.shortcuts import render, redirect, get_object_or_404
from .models import Consulta
from django.contrib.auth.decorators import login_required




def cadastrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta cadastrada com sucesso!")
            return redirect('listar_consultas')
        else:
            messages.error(request, "Erro ao cadastrar. Verifique os dados.")
    else:
        form = ConsultaForm()
    
    return render(request, 'Formularios/cad_Consulta.html', {'form': form})


@login_required
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