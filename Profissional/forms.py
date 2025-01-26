# forms.py
from django import forms
from .models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude
from users.models import Usuario
from especialidades.models import Especialidade  # Importando o modelo Especialidade

class CadastroProfissionalForm(forms.ModelForm):
    # Campos do modelo Usuario
    nome_completo = forms.CharField(max_length=150, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    telefone = forms.CharField(max_length=15, required=False)
    bairro = forms.CharField(max_length=255, required=False)
    rua = forms.CharField(max_length=255, required=False)
    complemento = forms.CharField(max_length=255, required=False)
    numerocasa = forms.CharField(max_length=30, required=False)
    data_nascimento = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)

    # Campos do modelo ProfissionalSaude
    especialidade = forms.ModelChoiceField(queryset=Especialidade.objects.all(), required=True)
    unidade_saude = forms.ModelChoiceField(queryset=UnidadeSaude.objects.all(), empty_label="Selecione uma Unidade de Saúde", required=True)

    class Meta:
        model = ProfissionalSaude
        fields = ['especialidade', 'unidade_saude']

    def clean(self):
        cleaned_data = super().clean()
        nome_completo = cleaned_data.get('nome_completo')

        if not nome_completo:
            raise forms.ValidationError('O campo nome completo é obrigatório.')

        # Retorna os dados limpos
        return cleaned_data

    def save(self, commit=True):
        # Cria o usuário primeiro
        usuario_data = {
            'username': self.cleaned_data['cpf'],  # Usando o CPF como username
            'nome_completo': self.cleaned_data['nome_completo'],
            'cpf': self.cleaned_data['cpf'],
            'telefone': self.cleaned_data['telefone'],
            'bairro': self.cleaned_data['bairro'],
            'rua': self.cleaned_data['rua'],
            'complemento': self.cleaned_data['complemento'],
            'numerocasa': self.cleaned_data['numerocasa'],
            'data_nascimento': self.cleaned_data['data_nascimento'],
            'email': self.cleaned_data['email'],
        }

        usuario = Usuario.objects.create(**usuario_data)
        usuario.set_password(self.cleaned_data['senha'])  # Criptografando a senha
        usuario.save()

        # Cria o profissional de saúde associado ao usuário
        profissional_data = {
            'usuario': usuario,
            'especialidade': self.cleaned_data['especialidade'],
            'unidade_saude': self.cleaned_data['unidade_saude'],
        }

        profissional = ProfissionalSaude.objects.create(**profissional_data)

        return profissional
