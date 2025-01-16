from django.shortcuts import render, redirect

from Paciente.forms import PacienteForm

def cadastro_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sucesso')  # Redirecionando para a página de sucesso
        else:
            return render(request, 'cadastro.html', {'form': form, 'erro': 'Erro ao cadastrar paciente'})
    else:
        form = PacienteForm()
    return render(request, 'cadastro.html', {'form': form})

def sucesso(request):
    return render(request, 'sucesso.html')  # Renderiza a página de sucesso
