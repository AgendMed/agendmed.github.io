from django import forms
from .models import Campanha

class CampanhaForm(forms.ModelForm):
    class Meta:
        model = Campanha
        fields = ['titulo', 'subtitulo', 'descricao', 'imagem', 'data_inicial', 'data_final', 'unidade_saude']
