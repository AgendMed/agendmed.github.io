// Scripts de cadastro
document.addEventListener('DOMContentLoaded', function() {
    var nome = document.getElementById('nome');
    var email = document.getElementById('emailCadastro');
    var senha = document.getElementById('senhaCadastro');
    var confirmarSenha = document.getElementById('confirmarSenha');

    var nomeError = document.getElementById('nomeError');
    var emailError = document.getElementById('emailError');
    var senhaError = document.getElementById('senhaError');
    var confirmarSenhaError = document.getElementById('confirmarSenhaError');

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    function validarFormulario(event) {
        nomeError.textContent= '';
        emailError.textContent = '';
        senhaError.textContent = '';
        confirmarSenhaError.textContent = '';

        let isValid = true;

        if (nome.value.trim() === '') {
            nomeError.textContent = 'Por favor, preencha o campo Nome.';
            isValid = false;
        }

        if (!emailRegex.test(email.value)) {
            emailError.textContent= 'Por favor, insira um email válido.';
            isValid = false;
        }

        if (senha.value.lenght < 6) {
            senhaError.textContent = 'A senha deve ter pelo menos 6 caracteres.';
            isValid = false;
        }

        if (senha.value !== confirmarSenha.value) {
            confirmarSenhaError.textContent = 'As senhas não coincidem.';
            isValid = false;
        }

        if (isValid) {
            const usuario = {
                nome: nome.value,
                email: email.value,
                senha: senha.value
            };

            localStorage.setItem('usuario', JSON.stringify(usuario));

            Swal.fire({
                title: 'Cadastro realizado!',
                text: 'Seus dados foram salvos com sucesso.',
                icon: 'success',
                time: 3000
            });

            nome.value = '';
            email.value = '';
            senha.value = '';
            confirmarSenha.value = '';
        }
    }

    var form = document.querySelector('form');
    form.addEventListener('submit', validarFormulario);
});
    


// Scripts de login