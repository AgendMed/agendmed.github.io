from django.shortcuts import render, redirect
from .forms import CadastroPacienteForm


def cadastrar_paciente(request):
    if request.method == "POST":
        form = CadastroPacienteForm(request.POST, request.FILES)
        if form.is_valid():
            # Salva o formulário e cria o paciente
            form.save()
            return redirect('sucesso')  # Redireciona para a página de sucesso (substitua 'sucesso' com a URL correta)
    else:
        form = CadastroPacienteForm()

    return render(request, 'cadastro_paciente.html', {'form': form})
