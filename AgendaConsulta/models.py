from django.db import models
from Paciente.models import Paciente
from Profissional.models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude

class Agendamento(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamentos')
    profissional = models.ForeignKey(ProfissionalSaude, on_delete=models.CASCADE, related_name='agendamentos')
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    horario = models.TimeField()
    fichas_normais = models.IntegerField(default=0)
    fichas_prioridade = models.IntegerField(default=0)

    def __str__(self):
        return f"Agendamento de {self.paciente.nome_completo} com {self.profissional.nome} em {self.data}"