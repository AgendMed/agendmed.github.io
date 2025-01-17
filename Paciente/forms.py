from django import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'nome_completo',
            'cartao_saude',
            'cpf',
            'data_nascimento',
            'telefone',
            'bairro',
            'rua',
            'num_casa',
            'complemento',
            'email',
            'senha',
            'condicao_prioritaria',
            'comprovante',
        ]
