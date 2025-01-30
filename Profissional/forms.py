from django import forms
from django.contrib.auth import get_user_model
from Profissional.models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude
from especialidades.models import Especialidade

class ProfissionalSaudeForm(forms.ModelForm):
    class Meta:
        model = ProfissionalSaude
        fields = ['nome', 'cpf', 'telefone', 'bairro', 'rua', 'complemento', 'numero_casa', 'data_nascimento', 'email', 'senha', 'especialidade', 'unidade_saude']

    nome = forms.CharField(max_length=100, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    telefone = forms.CharField(max_length=15, required=True)
    bairro = forms.CharField(max_length=100, required=True)
    rua = forms.CharField(max_length=100, required=True)
    complemento = forms.CharField(max_length=100, required=False)
    numero_casa = forms.IntegerField(required=True)
    data_nascimento = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput(), required=True)
    especialidade = forms.ModelChoiceField(queryset=Especialidade.objects.all(), required=True)
    unidade_saude = forms.ModelChoiceField(queryset=UnidadeSaude.objects.all(), required=True)

    def save(self, commit=True):
        # Criação do usuário
        usuario = get_user_model().objects.create_user(
            username=self.cleaned_data['cpf'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['senha'],
            nome_completo=self.cleaned_data['nome'],
            cpf=self.cleaned_data['cpf'],
            telefone=self.cleaned_data['telefone'],
            bairro=self.cleaned_data['bairro'],
            rua=self.cleaned_data['rua'],
            complemento=self.cleaned_data['complemento'],
            numerocasa=self.cleaned_data['numero_casa'],
            data_nascimento=self.cleaned_data['data_nascimento']
        )

        # Criando o profissional de saúde associado ao usuário
        profissional = super().save(commit=False)
        profissional.usuario = usuario

        if commit:
            profissional.save()

        return profissional
