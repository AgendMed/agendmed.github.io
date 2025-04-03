from django.contrib import messages
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
            #messages.success(request, "Campanha cadastrada com sucesso!")
            return redirect('Campanha:listar_campanhas')
        else:
            print('Formulário inválido')
            print(form.errors)
    else:
        form = CampanhaForm()
    
    return render(request, 'Formularios/cad_Campanha.html', {'form': form})
    

def listar_campanhas(request):
    campanhas = Campanha.objects.all()
    return render(request, 'campanha/listar_campanhas.html', {'campanhas': campanhas})




def editar_campanha(request, campanha_id):
    campanha = get_object_or_404(Campanha, id=campanha_id)
    
    if request.method == "POST":
        form = CampanhaForm(request.POST, request.FILES, instance=campanha)
        if form.is_valid():
            form.save()
            #messages.success(request, "Campanha atualizada com sucesso!")
            return redirect('Campanha:listar_campanhas')
        else:
            messages.error(request, "Corrija os erros abaixo.")
    else:
        form = CampanhaForm(instance=campanha)
    
    return render(request, 'campanha/edita_campanha.html', {
        'form': form,
        'campanha': campanha
    })



#@permission_required('campanha.pode_cadastrar_campanha')
def deletar_campanha(request, campanha_id):
    campanha = get_object_or_404(Campanha, id=campanha_id)
    if request.method == "POST":
        campanha.delete()
        return redirect('Campanha:listar_campanhas')
    return render(request, 'campanha/confirmar_exclusao.html', {'campanha': campanha})
