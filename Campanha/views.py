from django.shortcuts import render
from django.contrib.auth.decorators import permission_required

@permission_required('campanha.pode_cadastrar_campanha')
def cadastrar_campanha(request):
    return None
