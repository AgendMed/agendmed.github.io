from django.http import HttpResponse
from django.shortcuts import render, redirect

from especialidades.models import Especialidade
from .forms import EspecialidadeForm 

def cadastrar_especialidade(request):
    if request.method == 'POST':
        form = EspecialidadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso')  # Supondo que você tenha uma URL chamada 'sucesso'
    else:
        form = EspecialidadeForm()
    
    return render(request, 'Formularios/cad_especialidade.html', {'form': form})


def especialidade_sucesso(request):
    return HttpResponse("Especialidade cadastrada com sucesso!")

def listar_especialidades(request):
    especialidades = Especialidade.objects.all()
    return render(request, 'profissional/EscolhaConsulta.html', {'especialidades': especialidades})