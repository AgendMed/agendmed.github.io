from .models import Usuario, Paciente

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
