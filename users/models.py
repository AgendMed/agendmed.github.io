from datetime import date
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.decorators import permission_required
from django.shortcuts import render



class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=True, verbose_name='CPF', help_text='Obrigatório. 14 caracteres no formato XXX.XXX.XXX-XX')
    nome_completo = models.CharField(max_length=150, null=False, default='Nome não informado')
    cpf = models.CharField(max_length=30, unique=True)
    telefone = models.CharField(max_length=30, blank=True, null=False, default='Telefone não informado')
    data_nascimento = models.DateField(verbose_name="Data de nascimento", default=date(2000, 1, 1), null=False)
    bairro = models.CharField(max_length=255, blank=True, null=False, default='Bairro não informado')
    rua = models.CharField(max_length=255, blank=True, null=False, default='Rua não informada')
    complemento = models.CharField(max_length=255, blank=True, null=False, default='complemento não informado')
    numerocasa = models.CharField(max_length=20, null=False, default='Numero da Casa não informado')


    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.nome_completo

    @staticmethod
    @receiver(post_migrate)
    def criar_grupos_permissoes(sender, **kwargs):
        """
        Método estático para criar grupos e permissões automaticamente no banco de dados.
        """
        # Criar grupos
        grupo_medico, _ = Group.objects.get_or_create(name='Medico')
        grupo_paciente, _ = Group.objects.get_or_create(name='Paciente')
        grupo_unidade_saude, _ = Group.objects.get_or_create(name='Unidade_Saude')
        grupo_admin, _ = Group.objects.get_or_create(name='Admin')
        grupo_agente_saude, _ = Group.objects.get_or_create(name='Agente_Saude')

        content_type = ContentType.objects.get_for_model(Usuario)

        # Criar permissões para médicos e pacientes
        permissao_atender, _ = Permission.objects.get_or_create(
            codename='pode_atender',
            name='Pode atender consultas',
            content_type=content_type,
        )
        permissao_visualizar, _ = Permission.objects.get_or_create(
            codename='pode_visualizar_pacientes',
            name='Pode visualizar pacientes',
            content_type=content_type,
        )

        # Criar permissões para a Unidade de Saúde
        permissao_gerenciar_pacientes, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_pacientes',
            name='Pode gerenciar pacientes',
            content_type=content_type,
        )
        permissao_gerenciar_consultas, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_consultas',
            name='Pode gerenciar consultas',
            content_type=content_type,
        )

        # Criar permissões para administradores
        permissao_gerenciar_usuarios, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_usuarios',
            name='Pode gerenciar usuários',
            content_type=content_type,
        )
        permissao_gerenciar_unidades, _ = Permission.objects.get_or_create(
            codename='pode_gerenciar_unidades',
            name='Pode gerenciar unidades de saúde',
            content_type=content_type,
        )

        permissao_consultar, _ = Permission.objects.get_or_create(
            codename='pode_consultar',
            name='Pode consultar dados de pacientes',
            content_type=content_type,
        )
        
        grupo_paciente.permissions.add(permissao_consultar)

        # Criar permissões para o agente de saúde
        permissao_cadastrar_campanha, _ = Permission.objects.get_or_create(
            codename='pode_cadastrar_campanha',
            name='Pode cadastrar campanhas',
            content_type=content_type,
        )

        permissao_cadastrar_paciente, _ = Permission.objects.get_or_create(
            codename='pode_cadastrar_paciente',
            name='Pode cadastrar pacientes',
            content_type=content_type,
        )

        permissao_cadastrar_consulta, _ = Permission.objects.get_or_create(
            codename='pode_cadastrar_consulta',
            name='Pode cadastrar consultas',
            content_type=content_type,
        )

        grupo_agente_saude.permissions.add(permissao_cadastrar_campanha, permissao_cadastrar_paciente, permissao_cadastrar_consulta)
        grupo_medico.permissions.add(permissao_atender, permissao_visualizar)
        grupo_paciente.permissions.add(permissao_visualizar)
        grupo_unidade_saude.permissions.add(permissao_gerenciar_pacientes, permissao_gerenciar_consultas)
        grupo_admin.permissions.add(permissao_gerenciar_usuarios, permissao_gerenciar_unidades)

        print("Grupos e permissões criados com sucesso!")
