from django import forms
from .models import Usuario, Paciente




class CadastroPacienteForm(forms.ModelForm):
    # Campos do modelo Usuario
    nome_completo = forms.CharField(max_length=150, required=True)
    cpf = forms.CharField(max_length=14, required=True)
    telefone = forms.CharField(max_length=15, required=False)
    Bairro = forms.CharField(max_length=255, required=False)
    Rua = forms.CharField(max_length=255, required=False)
    complemento = forms.CharField(max_length=255, required=False)
    NumeroCasa = forms.CharField(max_length=30, required=False)
    data_nascimento = forms.DateField(required=True)
    email = forms.EmailField(required=True)
    senha = forms.CharField(widget=forms.PasswordInput, required=True)

    # Campos do modelo Paciente
    cartao_saude = forms.CharField(max_length=15, required=True)
    condicao_prioritaria = forms.ChoiceField(
        choices=Paciente._meta.get_field('condicao_prioritaria').choices, required=False)
    comprovante = forms.FileField(required=False)


    class Meta:
        model = Paciente
        fields = ['cartao_saude', 'condicao_prioritaria', 'comprovante']

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
            'Bairro': self.cleaned_data['Bairro'],
            'Rua': self.cleaned_data['Rua'],
            'complemento': self.cleaned_data['complemento'],
            'NumeroCasa': self.cleaned_data['NumeroCasa'],
            'data_nascimento': self.cleaned_data['data_nascimento'],
            'email': self.cleaned_data['email'],
        }

        usuario = Usuario.objects.create(**usuario_data)
        usuario.set_password(self.cleaned_data['senha'])  # Criptografando a senha
        usuario.save()


        # Cria o paciente associado ao usuário
        paciente_data = {
            'usuario': usuario,
            'cartao_saude': self.cleaned_data['cartao_saude'],
            'condicao_prioritaria': self.cleaned_data['condicao_prioritaria'],
            'comprovante': self.cleaned_data['comprovante'],
        }

        paciente = Paciente.objects.create(**paciente_data)

        return paciente
