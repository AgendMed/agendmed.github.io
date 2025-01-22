from django.db import models
from Unidade_Saude.models import UnidadeSaude

class ProfissionalSaude(models.Model):
    nome = models.CharField(max_length=100)
    especialidade = models.CharField(max_length=50)
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete=models.CASCADE, related_name='profissionais')

    def __str__(self):
        return f"{self.nome} - {self.especialidade}"