from django.shortcuts import render, redirect
from .forms import ProfissionalSaudeForm
<<<<<<< HEAD

def cadastro_profissional(request):
    if request.method == 'POST':
        form = ProfissionalSaudeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('sucesso')  # Redireciona para uma página de sucesso (ainda nao funciona)
    else:
        form = ProfissionalSaudeForm()

    return render(request, 'Formularios/cad_profissional.html', {'form': form})

=======
from django.contrib.auth.models import Group, Permission

def cadastro_profissional(request):
    if request.method == 'POST':
        form = ProfissionalSaudeForm(request.POST)
        if form.is_valid():
            profissional = form.save()

            # Verifica se a especialidade do profissional é 'Agente de Saúde'
            especialidade = profissional.especialidade.nome.lower()

            if especialidade == 'agente de saúde':
                grupo_agente_saude = Group.objects.get(name='Agente_Saude')
                profissional.usuario.groups.add(grupo_agente_saude)
                
                permissao_cadastrar_campanha = Permission.objects.get(codename='pode_cadastrar_campanha')
                permissao_cadastrar_paciente = Permission.objects.get(codename='pode_cadastrar_paciente')
                permissao_cadastrar_consulta = Permission.objects.get(codename='pode_cadastrar_consulta')
                profissional.usuario.user_permissions.add(permissao_cadastrar_campanha, permissao_cadastrar_paciente, permissao_cadastrar_consulta)
            
            # Caso contrário, assume-se que é um médico
            else:
                grupo_medico = Group.objects.get(name='Medico')
                profissional.usuario.groups.add(grupo_medico)
                
                permissao_atender = Permission.objects.get(codename='pode_atender')
                permissao_visualizar = Permission.objects.get(codename='pode_visualizar_pacientes')
                profissional.usuario.user_permissions.add(permissao_atender, permissao_visualizar)
            
            return redirect('sucesso')
    else:
        form = ProfissionalSaudeForm()

    return render(request, 'Formularios/cad_profissional.html', {'form': form})
>>>>>>> ed0684d553c3c83e57c0610639323e0c1eedf970
