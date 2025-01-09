from django.db import models
from django.core.validators import MinLengthValidator


class Paciente(models.Model):
    CONDMEDICA_CHOICES = [
        ('nenhuma','Não possui condição'),
        ('gravidez', 'Gravidez (Gestante)'),
        ('idoso', 'Idoso (60 anos ou mais)'),
        ('doencas_cronicas', 'Doenças Crônicas Graves'),
        ('urgencia', 'Urgências e Emergências'),
        ('deficiencia', 'Deficiências Físicas ou Mentais'),
        ('imunossupresso', 'Pacientes Imunossuprimidos'),
        ('doencas_infectocontagiosas', 'Doenças Infectocontagiosas'),
    ]
    
    condicao_prioritaria = models.CharField(max_length=50,
        choices=CONDMEDICA_CHOICES,
        default='nenhuma',  # Valor padrão
        )
    

    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    

    nomeCompleto = models.CharField(max_length=40)
    cartaoSaude = models.IntegerField()
    cpf = models.CharField(
        max_length=14,
        validators=[MinLengthValidator(11)],
        verbose_name="CPF",
    )
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    idade = models.IntegerField()
    telefone = models.CharField(max_length=15)
    bairro = models.CharField(max_length=25)
    rua = models.CharField(max_length=45)
    num_casa = models.IntegerField()
    complemento = models.CharField(max_length=100)
    email = models.EmailField(max_length=50, unique=True)
    senha = models.CharField(max_length=30)

def __str__(self):
        return self.cpf()


 
