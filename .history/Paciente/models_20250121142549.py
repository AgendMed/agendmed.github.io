from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class Paciente(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # Relaciona com o modelo de usuário personalizado
        on_delete=models.CASCADE,
        related_name='paciente'
    )
    cartao_saude = models.IntegerField(unique=True)
    data_nascimento = models.DateField(verbose_name="Data de nascimento")
    condicao_prioritaria = models.CharField(
        max_length=50,
        choices=[
            ('nenhuma', 'Não possui condição'),
            ('gravidez', 'Gravidez (Gestante)'),
            ('idoso', 'Idoso (60 anos ou mais)'),
            ('doencas_cronicas', 'Doenças Crônicas Graves'),
            ('urgencia', 'Urgências e Emergências'),
            ('deficiencia', 'Deficiências Físicas ou Mentais'),
            ('imunossupresso', 'Pacientes Imunossuprimidos'),
            ('doencas_infectocontagiosas', 'Doenças Infectocontagiosas'),
        ],
        default='nenhuma',
        null=True,
        blank=True
    )
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)

    def __str__(self):
        return self.usuario.paciente.usuario.nomeCompleto
