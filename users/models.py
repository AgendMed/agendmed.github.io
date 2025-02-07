from datetime import date
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.apps import apps


class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='CPF', help_text='Obrigatório. 14 caracteres no formato XXX.XXX.XXX-XX')
    nome_completo = models.CharField(max_length=150, null=False, default='Nome não informado')
    cpf = models.CharField(max_length=30, unique=True)
    telefone = models.CharField(max_length=30, blank=True, null=False, default='Telefone não informado')
    data_nascimento = models.DateField(verbose_name="Data de nascimento", default=date(2000, 1, 1), null=False)
    bairro = models.TextField(max_length=255, blank=True, null=False, default='Bairro não informado')
    rua = models.TextField(max_length=255, blank=True, null=False, default='Não informada')
    complemento = models.TextField(max_length=255, blank=True, null=False, default='Não informado')
    numerocasa = models.CharField(max_length=30, null=False, default='Não informado')
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.nome_completo

@receiver(post_migrate)
def criar_grupos_permissoes(sender, **kwargs):
    Paciente = apps.get_model('Paciente', 'Paciente')
    Consulta = apps.get_model('AgendaConsulta', 'Consulta')
    Campanha = apps.get_model('Campanha', 'Campanha')
    UnidadeSaude = apps.get_model('Unidade_Saude', 'UnidadeSaude')

    # Criar grupos
    grupo_medico, _ = Group.objects.get_or_create(name='Medico')
    grupo_paciente, _ = Group.objects.get_or_create(name='Paciente')
    grupo_unidade_saude, _ = Group.objects.get_or_create(name='Unidade_Saude')
    grupo_admin, _ = Group.objects.get_or_create(name='Admin')
    grupo_agente_saude, _ = Group.objects.get_or_create(name='Agente_Saude')

    content_type_usuario = ContentType.objects.get_for_model(Usuario)
    content_type_consulta = ContentType.objects.get_for_model(Consulta)
    content_type_campanha = ContentType.objects.get_for_model(Campanha)
    content_type_paciente = ContentType.objects.get_for_model(Paciente) 


    # Permissões para Agente de Saúde
    permissao_cadastrar_campanha, _ = Permission.objects.get_or_create(
        codename='pode_cadastrar_campanha',
        name='Pode cadastrar campanhas',
        content_type=content_type_campanha,
    )

    permissao_cadastrar_paciente, _ = Permission.objects.get_or_create(
        codename='pode_cadastrar_paciente',
        name='Pode cadastrar pacientes',
        content_type=content_type_paciente,
    )

    permissao_cadastrar_consulta, _ = Permission.objects.get_or_create(
        codename='pode_cadastrar_consulta',
        name='Pode cadastrar consultas',
        content_type=content_type_consulta,
    )

    grupo_agente_saude.permissions.add(
        permissao_cadastrar_campanha,
        permissao_cadastrar_paciente,
        permissao_cadastrar_consulta
    )

    # Permissões para Médico
    permissao_atender, _ = Permission.objects.get_or_create(
        codename='pode_atender',
        name='Pode atender pacientes',
        content_type=content_type_consulta,
    )

    permissao_visualizar_consultas, _ = Permission.objects.get_or_create(
        codename='pode_visualizar_consultas',
        name='Pode visualizar consultas',
        content_type=content_type_consulta,
    )

    permissao_visualizar_pacientes, _ = Permission.objects.get_or_create(
        codename='pode_visualizar_pacientes',
        name='Pode visualizar pacientes',
        content_type=content_type_paciente,
    )

    grupo_medico.permissions.add(
        permissao_atender,
        permissao_visualizar_consultas,
        permissao_visualizar_pacientes
    )

    # Permissões para Unidade de Saúde
    permissao_gerenciar_pacientes, _ = Permission.objects.get_or_create(
        codename='pode_gerenciar_pacientes',
        name='Pode gerenciar pacientes',
        content_type=content_type_paciente,
    )

    permissao_gerenciar_consultas, _ = Permission.objects.get_or_create(
        codename='pode_gerenciar_consultas',
        name='Pode gerenciar consultas',
        content_type=content_type_consulta,
    )

    grupo_unidade_saude.permissions.add(
        permissao_gerenciar_pacientes,
        permissao_gerenciar_consultas
    )

    # Permissões para Admin
    permissao_gerenciar_usuarios, _ = Permission.objects.get_or_create(
        codename='pode_gerenciar_usuarios',
        name='Pode gerenciar usuários',
        content_type=content_type_usuario,
    )

    permissao_gerenciar_unidades, _ = Permission.objects.get_or_create(
        codename='pode_gerenciar_unidades',
        name='Pode gerenciar unidades de saúde',
        content_type=ContentType.objects.get_for_model(UnidadeSaude),
    )

    grupo_admin.permissions.add(
        permissao_gerenciar_usuarios,
        permissao_gerenciar_unidades
    )

    # Permissões para Paciente
    permissao_agendar_consulta, _ = Permission.objects.get_or_create(
        codename='pode_agendar_consulta',
        name='Pode agendar consulta',
        content_type=content_type_consulta,
    )

    grupo_paciente.permissions.add(permissao_agendar_consulta)

    print("Grupos e permissões criados com sucesso!")