#views.py
from django.shortcuts import render, redirect
from .forms import UnidadeSaudeForm

def cadastro_unidade_saude(request):
    if request.method == 'POST':
        form = UnidadeSaudeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('UnidadeSaude:sucesso')
        else:
            
            return render(request, 'Formularios/cad_UnidadeSaude.html', {'form': form})
    else:
        
        form = UnidadeSaudeForm()
        return render(request, 'Formularios/cad_UnidadeSaude.html', {'form': form})


def sucesso(request):
    return render(request, 'sucesso.html')
