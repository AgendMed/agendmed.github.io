from django import forms
from django.contrib.auth import get_user_model
from Profissional.models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude
from especialidades.models import Especialidade
import requests
from django.core.exceptions import ValidationError

class ProfissionalSaudeForm(forms.ModelForm):
    class Meta:
        model = ProfissionalSaude
        fields = ['nome', 'cpf', 'telefone', 'bairro', 'rua', 'complemento', 'numero_casa', 
                 'data_nascimento', 'email', 'senha', 'especialidade', 'unidade_saude']

    nome = forms.CharField(max_length=100, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    telefone = forms.CharField(max_length=15, required=True)
    cep = forms.CharField(max_length=9, required=True)
    bairro = forms.CharField(max_length=100, required=True)
    rua = forms.CharField(max_length=100, required=True)
    complemento = forms.CharField(max_length=100, required=False)
    numero_casa = forms.IntegerField(required=True)
    data_nascimento = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput(), required=True)
    especialidade = forms.ModelChoiceField(queryset=Especialidade.objects.all(), required=True)
    unidade_saude = forms.ModelChoiceField(queryset=UnidadeSaude.objects.all(), required=True)

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

        endereco_completo = f"{self.cleaned_data['rua']}, {self.cleaned_data['numero_casa']}, " \
                            f"{self.cleaned_data['bairro']}, {self.cleaned_data['cep']}"
        latitude, longitude = self.get_coordinates(endereco_completo)
        
        if latitude is None or longitude is None:
            raise ValidationError("Não foi possível obter as coordenadas para o endereço informado.")

        # Atualiza coordenadas do usuário
        usuario.latitude = latitude
        usuario.longitude = longitude
        usuario.save()

        profissional = super().save(commit=False)
        profissional.usuario = usuario

        if commit:
            profissional.save()

        return profissional