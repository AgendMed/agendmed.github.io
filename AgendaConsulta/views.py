from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ConsultaForm

def cadastrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consulta cadastrada com sucesso!")
            return redirect('listar_consultas')  # Não ajustada
        else:
            messages.error(request, "Erro ao cadastrar a consulta. Verifique os dados informados.")
    else:
        form = ConsultaForm()

    return render(request, 'Formularios/cad_Consulta.html', {'form': form})
