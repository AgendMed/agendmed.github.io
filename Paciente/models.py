from django.db import models
from Unidade_Saude.models import UnidadeSaude
from users.models import Usuario


class Paciente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cartao_saude = models.IntegerField(unique=True)
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
    
    is_prioritario_aprovado = models.BooleanField(default=False)

    def comprovante_atual(self):
        """ Retorna o último comprovante pendente ou aprovado do paciente. """
        return self.comprovantes.filter(status__in=["pendente", "aprovado"]).last()

    def __str__(self):
        return self.usuario.nome_completo


class ComprovanteValidacao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="comprovantes")
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete=models.CASCADE, related_name="comprovantes")
    arquivo = models.FileField(upload_to="comprovantes/")
    STATUS_CHOICES = [
        ("pendente", "Pendente"),
        ("aprovado", "Aprovado"),
        ("rejeitado", "Rejeitado"),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pendente")
    created_at = models.DateTimeField(auto_now_add=True)        # Adicionando timestamp para histórico

    def aprovar(self):
        """ Aprova o comprovante e define o paciente como prioritário """
        self.status = "aprovado"
        self.paciente.is_prioritario_aprovado = True
        self.paciente.save()
        self.save()

    def rejeitar(self):
        """ Rejeita o comprovante e remove status prioritário do paciente """
        self.status = "rejeitado"
        self.paciente.is_prioritario_aprovado = False
        self.paciente.save()
        self.save()

    def __str__(self):
        return f"Comprovante de {self.paciente.usuario.nome_completo} - {self.get_status_display()}"
