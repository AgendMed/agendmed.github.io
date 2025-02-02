from django.db import models
from users.models import Usuario

class Paciente(models.Model):
    STATUS_CHOICES = [
        ('comum', 'Comum'),
        ('prioritario', 'Prioritário'),
    ]
    
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cartao_saude = models.IntegerField(unique=True)
    status = models.CharField(
        max_length=11,
        choices=STATUS_CHOICES,
        default='comum'
    )
    condicao_prioritaria = models.CharField(
        max_length=50,
        choices=[
            ('nenhuma', 'Não possui condição'),
            ('gravidez', 'Gravizzação (Gestante)'),
            ('idoso', 'Idoso (60 anos ou mais)'),
            ('doencas_cronicas', 'Doenças Crônicas Graves'),
            ('urgencia', 'Urgências e Emergências'),
            ('deficiencia', 'Deficiências Físicas ou Mentais'),
            ('imunossupresso', 'Pacientes Imunossuprimidos'),
            ('doencas_infectocontagiosas', 'Doenças Infectocontagiosas'),
        ],
        default='nenhuma'
    )
    comprovante = models.FileField(upload_to='comprovantes/', null=True, blank=True)
    data_aprovacao = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.usuario.nome_completo} ({self.status})"