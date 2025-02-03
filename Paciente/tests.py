from django.test import TestCase
from .models import Paciente
from users.models import Usuario

class UsuarioTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="testuser",
            password="password123",
            nome_completo="Teste Completo",
            cpf="123.456.789-00"
        )

    def test_usuario_criado(self):
        self.assertEqual(self.usuario.nome_completo, "Teste Completo")
        self.assertTrue(self.usuario.check_password("password123"))

class PacienteTestCase(TestCase):
    def setUp(self):
        self.usuario = Usuario.objects.create_user(
            username="paciente1",
            password="senha123",
            nome_completo="Paciente Teste",
            cpf="987.654.321-00"
        )
        self.paciente = Paciente.objects.create(
            usuario=self.usuario,
            cartao_saude="1234567890"
        )

    def test_paciente_criado(self):
        self.assertEqual(self.paciente.usuario.nome_completo, "Paciente Teste")
