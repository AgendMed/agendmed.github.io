from django import forms
from django.shortcuts import render, redirect
from .forms import UnidadeSaudeForm

def cadastro_unidade_saude(request):
    if request.method == 'POST':
        form = UnidadeSaudeForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('UnidadeSaude:sucesso')
            except forms.ValidationError as e:
                form.add_error(None, e.message)
        else:
            print("Erros de formulário:", form.errors)
        return render(request, 'formularios/cad_UnidadeSaude.html', {'form': form})
    else:
        form = UnidadeSaudeForm()
    return render(request, 'formularios/cad_UnidadeSaude.html', {'form': form})

def sucesso(request):
    return render(request, 'sucesso.html')
