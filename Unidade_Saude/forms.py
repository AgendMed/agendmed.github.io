from django import forms
from .models import UnidadeSaude
import requests

class UnidadeSaudeForm(forms.ModelForm):
    nome = forms.CharField(max_length=100, required=True, label="Nome da Unidade")
    cep = forms.CharField(max_length=10, required=True, label="CEP")
    rua = forms.CharField(max_length=100, required=True, label="Rua")
    numero = forms.CharField(max_length=10, required=True, label="Número")
    telefone = forms.CharField(max_length=15, required=False, label="Telefone")
    email = forms.EmailField(required=True, label="E-mail")

    class Meta:
        model = UnidadeSaude
        fields = ['nome', 'telefone', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UnidadeSaude.objects.filter(email=email).exists():
            raise forms.ValidationError('Já existe uma unidade de saúde cadastrada com este e-mail.')
        return email

    def get_coordinates(self, address):
        """Consulta a API para obter latitude e longitude a partir do endereço."""
        API_KEY = "j7EFwWOjGiFXvA6bZDH6iNdbuCkuzB1K5caRlJ6jpnwRynXsW9fUY8mNCkyvYYk6"  # Substitua pela sua chave
        GEOCODING_API_URL = "https://api.distancematrix.ai/maps/api/geocode/json"
        params = {
            "address": address,
            "key": API_KEY,
        }

        try:
            # Remover espaços extras e normalizar o formato do endereço
            address = address.strip().replace(" ", "+")
            response = requests.get(GEOCODING_API_URL, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            # Debug: Imprimir resposta para verificar os dados retornados
            print("Resposta da API:", data)

            # Verifique o que a API retorna
            if data.get("status") != "OK":
                error_message = data.get("error_message", "Nenhum erro específico.")
                raise ValueError(f"Erro da API: {data.get('status')}. Detalhes: {error_message}")

            # Verifique se 'results' contém dados válidos
            if 'result' in data and data["result"]:
                result = data["result"][0]  # Corrigido para 'result'
                # Exibir detalhes da resposta
                print("Resultado da API:", result)

                location = result.get("geometry", {}).get("location", {})
                latitude = location.get("lat")
                longitude = location.get("lng")
                
                # Garantir que as coordenadas sejam extraídas corretamente
                if latitude is not None and longitude is not None:
                    return latitude, longitude
                else:
                    raise ValueError("A API retornou a localização, mas sem latitude e longitude válidas.")
            else:
                raise ValueError("Nenhum resultado encontrado para o endereço fornecido.")

        except requests.exceptions.RequestException as e:
            print(f"Erro ao consultar a API: {e}")
        except ValueError as e:
            print(f"Erro de valor: {e}")
        
        return None, None


    def save(self, commit=True):
        unidade = super().save(commit=False)

        # Concatenar o endereço completo
        cep = self.cleaned_data.get('cep')
        rua = self.cleaned_data.get('rua')
        numero = self.cleaned_data.get('numero')
        endereco_completo = f"{rua}, {numero}, {cep}"
        unidade.endereco = endereco_completo

        # Obter latitude e longitude
        latitude, longitude = self.get_coordinates(endereco_completo)
        if latitude and longitude:
            unidade.latitude = latitude
            unidade.longitude = longitude
        else:
            raise forms.ValidationError(
                'Não foi possível localizar o endereço. Verifique os detalhes informados.'
            )

        if commit:
            unidade.save()
        return unidade
