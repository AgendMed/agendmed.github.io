from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

User  = get_user_model()

class CPFBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Tente encontrar o usuário pelo CPF
            user = User.objects.get(cpf=username)
        except User.DoesNotExist:
            return None

        # Verifique a senha
        if user.check_password(password):
            return user
        return None