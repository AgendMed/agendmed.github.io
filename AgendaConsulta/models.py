from django.db import models
from Paciente.models import Paciente
from Profissional.models import ProfissionalSaude
from Unidade_Saude.models import UnidadeSaude

class Consulta(models.Model):
    unidade_saude = models.ForeignKey(UnidadeSaude, on_delete=models.CASCADE, related_name='consultas')
    profissional = models.ForeignKey(ProfissionalSaude, on_delete=models.CASCADE, related_name='consultas')
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    qtd_fichas_prioritarias = models.PositiveIntegerField(default=0)
    qtd_fichas_normais = models.PositiveIntegerField(default=0)
    lista_espera_prioritaria = models.ManyToManyField(Paciente, related_name='espera_prioritaria', blank=True)
    lista_espera_comum = models.ManyToManyField(Paciente, related_name='espera_comum', blank=True)

    def __str__(self):
        return f"Consulta com {self.profissional.usuario.nome_completo} em {self.data} às {self.horario}"


class Agendamento(models.Model):
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name='agendamentos')
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamentos')
    data_agendamento = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Agendamento de {self.paciente.usuario.nome_completo} para a consulta {self.consulta}"
