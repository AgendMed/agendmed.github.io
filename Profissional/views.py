from django.shortcuts import render, redirect
from .forms import ProfissionalSaudeForm

def cadastrar_profissional(request):
    if request.method == 'POST':
        form = ProfissionalSaudeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso')  # Redireciona para uma página de sucesso/ fazer pagina estatica
    else:
        form = ProfissionalSaudeForm()

    return render(request, 'Formularios/cad_ProfissionalSaude.html', {'form': form})
