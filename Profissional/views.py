from django.shortcuts import render, redirect
from .forms import CadastroProfissionalForm

def cadastro_profissional(request):
    if request.method == 'POST':
        form = CadastroProfissionalForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('sucesso')  # Alterar para o caminho que você desejar após sucesso
            except Exception as e:
                print("Erro:", e)
        else:
            print("Erros de formulário:", form.errors)
    else:
        form = CadastroProfissionalForm()
    return render(request, 'Formularios/cad_profissional.html', {'form': form})
