from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from .models import Consulta, Agendamento
from .forms import ConsultaForm, AgendamentoForm
from django.db.models import F


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

def agendar_consulta(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    consulta = Consulta.objects.select_for_update().get(
                        pk=form.cleaned_data['consulta'].id
                    )
                    paciente = form.cleaned_data['paciente']
                    
                    # Verifica e atualiza as fichas 
                    if paciente.status == 'prioritario':
                        if consulta.qtd_fichas_prioritarias < 1:
                            raise ValueError("Não há fichas prioritárias disponíveis")
                        consulta.qtd_fichas_prioritarias = F('qtd_fichas_prioritarias') - 1
                    else:
                        if consulta.qtd_fichas_normais < 1:
                            raise ValueError("Não há fichas normais disponíveis")
                        consulta.qtd_fichas_normais = F('qtd_fichas_normais') - 1
                    
                    consulta.save(update_fields=['qtd_fichas_prioritarias', 'qtd_fichas_normais'])
                    form.save()
                    
                    messages.success(request, 'Agendamento realizado com sucesso!')
                    return redirect('listar_consultas')
            
            except Exception as e:
                messages.error(request, str(e))
                return redirect('agendar_consulta')
        else:
            messages.error(request, 'Por favor corrija os erros no formulário')
    else:
        form = AgendamentoForm()
    
    return render(request, 'Paciente/AgendarConsulta.html', {'form': form})



#teste de listar consultas (incompleta)


def listar_consultas(request):
    consultas = Consulta.objects.all().annotate(
        total_fichas=F('qtd_fichas_prioritarias') + F('qtd_fichas_normais')
    )
    return render(request, 'lista_consultas.html', {'consultas': consultas})