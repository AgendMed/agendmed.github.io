from django.shortcuts import render

# View para a página do Admin
def pagina_admin(request):
    return render(request, 'admin.html')

# View para a página do Médico
def pagina_medico(request):
    return render(request, 'medico.html')

# View para a página do Paciente
def pagina_paciente(request):
    return render(request, 'paciente.html')
