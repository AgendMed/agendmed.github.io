from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Campanha
from .forms import CampanhaForm

#@permission_required('campanha.pode_cadastrar_campanha')
def cadastrar_campanha(request):
    if request.method == "POST":
        print('Recebeu POST')
        form = CampanhaForm(request.POST, request.FILES)
        if form.is_valid():
            print('Formulário válido')
            nova_campanha = form.save()
            print(f'Campanha salva: ID {nova_campanha.id}')
            return redirect('Campanha:listar_campanhas')
        else:
            print('Formulário inválido')
            print(form.errors)  # Mostra os erros no console
    else:
        form = CampanhaForm()
    
    return render(request, 'Formularios/cad_Campanha.html', {'form': form})
    

def listar_campanhas(request):
    campanhas = Campanha.objects.all()
    return render(request, 'campanha/listar_campanhas.html', {'campanhas': campanhas})

#@permission_required('campanha.pode_cadastrar_campanha')
def deletar_campanha(request, campanha_id):
    campanha = get_object_or_404(Campanha, id=campanha_id)
    if request.method == "POST":
        campanha.delete()
        return redirect('Campanha:listar_campanhas')
    return render(request, 'campanha/confirmar_exclusao.html', {'campanha': campanha})
