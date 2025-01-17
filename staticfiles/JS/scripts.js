// Scripts de cadastro
document.addEventListener('DOMContentLoaded', function() {
    var nome = document.getElementById('nome_completo');
    var cartaoSaude = document.getElementById('cartao_saude');
    var cpf = document.getElementById('cpf');
    var dataNascimento = document.getElementById('data_nascimento');
    var telefone = document.getElementById('telefone');
    var bairro = document.getElementById('bairro');
    var rua = document.getElementById('rua');
    var numCasa = document.getElementById('num_casa');
    var complemento = document.getElementById('complemento');
    var email = document.getElementById('email');
    var senha = document.getElementById('senha');
    var confirmarSenha = document.getElementById('confirmarSenha');
    var condicaoPrioritaria = document.getElementById('condicao_prioritaria');
    var comprovante = document.getElementById('comprovante');

    var nomeError = document.getElementById('nomeError');
    var cartaoSaudeError = document.getElementById('cartaoSaudeError');
    var cpfError = document.getElementById('cpfError');
    var dataNascimentoError = document.getElementById('dataNascimentoError');
    var telefoneError = document.getElementById('telefoneError');
    var bairroError = document.getElementById('bairroError');
    var ruaError = document.getElementById('ruaError');
    var numCasaError = document.getElementById('numCasaError');
    var emailError = document.getElementById('emailError');
    var senhaError = document.getElementById('senhaError');
    var confirmarSenhaError = document.getElementById('confirmarSenhaError');

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    function validarFormulario(event) {
        event.preventDefault();
        
        nomeError.textContent = '';
        cartaoSaudeError.textContent = '';
        cpfError.textContent = '';
        dataNascimentoError.textContent = '';
        telefoneError.textContent = '';
        bairroError.textContent = '';
        ruaError.textContent = '';
        numCasaError.textContent = '';
        emailError.textContent = '';
        senhaError.textContent = '';
        confirmarSenhaError.textContent = '';

        let isValid = true;

        if (nome.value.trim() === '') {
            nomeError.textContent = 'Por favor, preencha o campo Nome Completo.';
            isValid = false;
        } else {
            nome.style.borderColor = 'green';
        }

        if (cartaoSaude.value.trim() === '') {
            cartaoSaudeError.textContent = 'Por favor, preencha o campo Cartão de Saúde.';
            isValid = false;
        } else {
            cartaoSaude.style.borderColor = 'green';
        }

        if (!/^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(cpf.value)) {
            cpfError.textContent = 'Por favor, insira um CPF válido (ex: 000.000.000-00).';
            isValid = false;
        } else {
            cpf.style.borderColor = 'green';
        }

        if (dataNascimento.value === '') {
            dataNascimentoError.textContent = 'Por favor, preencha o campo Data de Nascimento.';
            isValid = false;
        } else {
            dataNascimento.style.borderColor = 'green';
        }

        if (telefone.value.trim() === '') {
            telefoneError.textContent = 'Por favor, preencha o campo Telefone.';
            isValid = false;
        } else {
            telefone.style.borderColor = 'green';
        }

        if (bairro.value.trim() === '') {
            bairroError.textContent = 'Por favor, preencha o campo Bairro.';
            isValid = false;
        } else {
            bairro.style.borderColor = 'green';
        }

        if (rua.value.trim() === '') {
            ruaError.textContent = 'Por favor, preencha o campo Rua.';
            isValid = false;
        } else {
            rua.style.borderColor = 'green';
        }

        if (numCasa.value.trim() === '') {
            numCasaError.textContent = 'Por favor, preencha o campo Número da Casa.';
            isValid = false;
        } else {
            numCasa.style.borderColor = 'green';
        }

        if (complemento.value.trim() !== '') {
            complemento.style.borderColor = 'green';
        }

        if (!emailRegex.test(email.value)) {
            emailError.textContent = 'Por favor, insira um email válido.';
            isValid = false;
        }

        if (senha.value.length < 6) {
            senhaError.textContent = 'A senha deve ter pelo menos 6 caracteres.';
            isValid = false;
        }

        if (senha.value !== confirmarSenha.value) {
            confirmarSenhaError.textContent = 'As senhas não coincidem.';
            isValid = false;
        }

        if (isValid) {
            // Aqui você pode enviar o formulário para o servidor
            // Formulário válido, você pode fazer o envio via AJAX ou enviar normalmente com o formulário.
            Swal.fire({
                title: 'Cadastro realizado!',
                text: 'Seus dados foram salvos com sucesso.',
                icon: 'success',
                timer: 3000
            });

            // Limpar os campos do formulário após o sucesso
            nome.value = '';
            cartaoSaude.value = '';
            cpf.value = '';
            dataNascimento.value = '';
            telefone.value = '';
            bairro.value = '';
            rua.value = '';
            numCasa.value = '';
            complemento.value = '';
            email.value = '';
            senha.value = '';
            confirmarSenha.value = '';
        }
    }

    var form = document.querySelector('form');
    form.addEventListener('submit', validarFormulario);
});
