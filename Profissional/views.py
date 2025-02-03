from django.shortcuts import render, redirect
from .forms import ProfissionalSaudeForm

def cadastro_profissional(request):
    if request.method == 'POST':
        form = ProfissionalSaudeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso')  # Redireciona para uma página de sucesso (ainda nao funciona)
    else:
        form = ProfissionalSaudeForm()

    return render(request, 'Formularios/cad_profissional.html', {'form': form})

def profissional_home(request):
    return render(request, 'home.html')
