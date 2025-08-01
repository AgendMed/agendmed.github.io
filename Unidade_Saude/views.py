from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UnidadeSaudeForm
from .models import UnidadeSaude
from django.contrib.auth.decorators import permission_required, login_required


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



def detalhe_unidade_saude(request, pk):
    unidade = get_object_or_404(UnidadeSaude, pk=pk)
    return render(request, 'UnidadeSaude/detalhe_unidade_saude.html', {'unidade': unidade})


@login_required
def editar_unidade_saude(request, pk):
    unidade = get_object_or_404(UnidadeSaude, pk=pk)

    if request.method == 'POST':
        form = UnidadeSaudeForm(request.POST, instance=unidade)
        if form.is_valid():
            form.save()
            return redirect('UnidadeSaude:detalhe_unidade', pk=pk)
    else:
        form = UnidadeSaudeForm(instance=unidade)

    return render(request, 'UnidadeSaude/editar_UnidadeSaude.html', {'form': form, 'unidade': unidade})
