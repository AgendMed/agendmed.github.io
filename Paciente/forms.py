from django import forms
import requests

from Unidade_Saude.models import UnidadeSaude
from .models import Usuario, Paciente
from users.models import Usuario
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import PasswordChangeForm

class CadastroPacienteForm(forms.ModelForm):
    nome_completo = forms.CharField(max_length=150, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    telefone = forms.CharField(max_length=15, required=False)
    cep = forms.CharField(max_length=9, required=True)
    bairro = forms.CharField(max_length=255, required=False)
    rua = forms.CharField(max_length=255, required=False)
    complemento = forms.CharField(max_length=255, required=False)
    numerocasa = forms.CharField(max_length=30, required=False)
    data_nascimento = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)
    cartao_saude = forms.CharField(max_length=15, required=True)
    condicao_prioritaria = forms.ChoiceField(
        choices=Paciente._meta.get_field('condicao_prioritaria').choices, required=False
    )
    comprovante = forms.FileField(required=False)
    unidade_saude = forms.ModelChoiceField(
        queryset=UnidadeSaude.objects.all(),
        required=True,
        label="Unidade de Saúde"
    )

    class Meta:
        model = Paciente
        fields = ['status', 'condicao_prioritaria', 'comprovante', 'data_aprovacao', 'unidade_saude']

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('nome_completo'):
            raise ValidationError('O campo Nome Completo é obrigatório.')
        if not cleaned_data.get('cpf'):
            raise ValidationError('O CPF é obrigatório.')
        if not cleaned_data.get('email'):
            raise ValidationError('O E-mail é obrigatório.')
        comprovante = cleaned_data.get('comprovante')
        if comprovante and not comprovante.name.endswith(('.pdf', '.jpg', '.png')):
            raise ValidationError('O arquivo de comprovante deve ser PDF, JPG ou PNG.')
        return cleaned_data

    def get_coordinates(self, address):
        API_KEY = "j7EFwWOjGiFXvA6bZDH6iNdbuCkuzB1K5caRlJ6jpnwRynXsW9fUY8mNCkyvYYk6"
        GEOCODING_API_URL = "https://api.distancematrix.ai/maps/api/geocode/json"
        params = {"address": address, "key": API_KEY}
        
        try:
            response = requests.get(GEOCODING_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "OK":
                print("Erro na API:", data)
                return None, None

            results = data.get("result", [])
            if not results:
                print("Nenhum resultado encontrado:", data)
                return None, None

            location = results[0].get("geometry", {}).get("location", {})
            lat, lng = location.get("lat"), location.get("lng")

            if lat == 0 and lng == 0:
                print("Coordenadas inválidas para o endereço:", address)
                return None, None

            return lat, lng

        except requests.exceptions.RequestException as e:
            print("Erro na requisição:", e)
            return None, None

    def save(self, commit=True):
        # Cria o usuário
        usuario = Usuario.objects.create_user(
            username=self.cleaned_data['cpf'],
            nome_completo=self.cleaned_data['nome_completo'],
            cpf=self.cleaned_data['cpf'],
            telefone=self.cleaned_data['telefone'],
            bairro=self.cleaned_data['bairro'],
            rua=self.cleaned_data['rua'],
            complemento=self.cleaned_data['complemento'],
            numerocasa=self.cleaned_data['numerocasa'],
            data_nascimento=self.cleaned_data['data_nascimento'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['senha']
        )

        endereco_completo = f"{self.cleaned_data['rua']}, {self.cleaned_data['numerocasa']}, {self.cleaned_data['bairro']}, {self.cleaned_data['cep']}"
        latitude, longitude = self.get_coordinates(endereco_completo)

        if latitude is None or longitude is None:
            raise ValidationError("Não foi possível obter as coordenadas para o endereço informado.")

        # Atribui as coordenadas ao usuário
        usuario.latitude = latitude
        usuario.longitude = longitude
        usuario.save()

        # Cria o paciente
        paciente = Paciente.objects.create(
            usuario=usuario,
            cartao_saude=self.cleaned_data['cartao_saude'],
            condicao_prioritaria=self.cleaned_data['condicao_prioritaria'],
            comprovante=self.cleaned_data['comprovante'],
            unidade_saude=self.cleaned_data['unidade_saude'],
            status='comum'
        )

        return paciente

class UsuarioForm(forms.ModelForm):
    senha_atual = forms.CharField(widget=forms.PasswordInput, required=False)
    nova_senha = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Usuario
        fields = ['nome_completo', 'telefone', 'data_nascimento', 'bairro', 'rua', 'complemento', 'numerocasa', 'senha_atual', 'nova_senha']  # Excluindo CPF

    def clean(self):
        cleaned_data = super().clean()
        senha_atual = cleaned_data.get('senha_atual')
        nova_senha = cleaned_data.get('nova_senha')

        if senha_atual and not self.instance.check_password(senha_atual):
            raise ValidationError("A senha atual está incorreta.")

        if nova_senha and len(nova_senha) < 6:
            raise ValidationError("A nova senha deve ter pelo menos 6 caracteres.")

        return cleaned_data

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['cartao_saude', 'condicao_prioritaria']  # Campos que podem ser editados