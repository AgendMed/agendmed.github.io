from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(f"Usuário autenticado: {user}")  
            
            login(request, user)
            if user.groups.filter(name='Admin').exists():
                print("Redirecionando para admin:dashboard")
                return redirect('admin:dashboard')
            elif user.groups.filter(name__in=['Medico', 'Agente_Saude']).exists():
                print("Redirecionando para profissional:paginainicial")
                return redirect('profissional:paginainicial')
            elif user.groups.filter(name='Paciente').exists():
                print("Redirecionando para Paciente:agendar_consulta")
                return redirect('Paciente:agendar_consulta')
            else:
                print("Redirecionando para página padrão")
                return redirect('pagina_padrao')
        else:
            print("Erro: Credenciais inválidas")
            print(f"Erros de Formulário: {form.errors}")
            messages.error(request, "Credenciais inválidas!")
    else:
        form = AuthenticationForm()

    return render(request, 'Login/login.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    return redirect('users:login')