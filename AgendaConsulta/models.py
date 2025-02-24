from django.db import models

from django.db import models

class Consulta(models.Model):
    unidade_saude = models.ForeignKey(
        'Unidade_Saude.UnidadeSaude',
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    profissional = models.ForeignKey(
        'Profissional.ProfissionalSaude',
        on_delete=models.CASCADE,
        related_name='consultas'
    )
    data = models.DateField()
    horario_inicio = models.TimeField()
    horario_fim = models.TimeField()
    qtd_fichas_prioritarias = models.PositiveIntegerField(default=0)
    qtd_fichas_normais = models.PositiveIntegerField(default=0)
    lista_espera_prioritaria = models.ManyToManyField(
        'Paciente.Paciente',
        related_name='espera_prioritaria',
        blank=True
    )
    lista_espera_comum = models.ManyToManyField(
        'Paciente.Paciente',
        related_name='espera_comum',
        blank=True
    )

    class Meta:
        permissions = [
            ("pode_agendar_consulta", "Pode agendar consultas"),
            ("pode_gerenciar_consultas", "Pode gerenciar consultas"),
            ("pode_atender", "Pode atender pacientes"),
        ]

    def __str__(self):
        return f"Consulta {self.id} - {self.data} ({self.horario_formatado})"

    @property
    def horario_formatado(self):
        return f"{self.horario_inicio.strftime('%H:%M')} às {self.horario_fim.strftime('%H:%M')}"

class Agendamento(models.Model):
    
    consulta = models.ForeignKey(
        'Consulta',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )
    paciente = models.ForeignKey(
        'Paciente.Paciente',
        on_delete=models.CASCADE,
        related_name='agendamentos'
    )
    data_agendamento = models.DateTimeField(auto_now_add=True)
    numero_na_fila = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Agendamento {self.id} - {self.paciente} para {self.consulta}"
    

from django.db import models
from Paciente.models import Paciente

class Notificacao(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='notificacoes')
    mensagem = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    lida = models.BooleanField(default=False)

    def __str__(self):
        return f"Notificação para {self.paciente.usuario.nome_completo} - {self.mensagem[:50]}..."