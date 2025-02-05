document.addEventListener('DOMContentLoaded', function() {
    var nome = document.getElementById('nome_completo'); 
    var cartSus = document.getElementById('cartao_saude'); 
    var cpf = document.getElementById('cpf');
    var dataNascimento = document.getElementById('data_nascimento'); 
    var telefone = document.getElementById('telefone');
    var bairro = document.getElementById('bairro');
    var rua = document.getElementById('rua');
    var email = document.getElementById('email'); 
    var senha = document.getElementById('senha'); 
    var confirmarSenha = document.getElementById('confirmar_senha');
    
    var condicaoPrioritaria = document.getElementById('condicao_prioritaria');
    var comprovanteField = document.getElementById('comprovante');

    var nomeError = document.getElementById('nomeError');
    var cartaoSaudeError = document.getElementById('cartaoSaudeError');
    var cpfError = document.getElementById('cpfError');
    var dataNascimentoError = document.getElementById('dataNascimentoError');
    var telefoneError = document.getElementById('telefoneError');
    var bairroError = document.getElementById('bairroError');
    var ruaError = document.getElementById('ruaError');
    var emailError = document.getElementById('emailError');
    var senhaError = document.getElementById('senhaError');
    var confirmarSenhaError = document.getElementById('confirmarSenhaError');

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    function validarFormulario(event) {
        // Limpar erros anteriores
        nomeError.textContent = '';
        cartaoSaudeError.textContent = '';
        cpfError.textContent = '';
        dataNascimentoError.textContent = '';
        telefoneError.textContent = '';
        bairroError.textContent = '';
        ruaError.textContent = '';
        emailError.textContent = '';
        senhaError.textContent = '';
        confirmarSenhaError.textContent = '';

        let isValid = true;

        // Validações dos campos
        if (nome.value.trim() === '') {
            nomeError.textContent = 'Por favor, preencha o campo Nome.';
            isValid = false;
        } else {
            nome.style.borderColor = 'green';
        }

        if (cartSus.value.trim() === '') {
            cartaoSaudeError.textContent = 'Por favor, preencha o campo Cartão SUS.';
            isValid = false;
        } else {
            cartSus.style.borderColor = 'green';
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

        if (!emailRegex.test(email.value)) {
            emailError.textContent = 'Por favor, insira um email válido.';
            isValid = false;
        } else {
            email.style.borderColor = 'green';
        }

        if (senha.value.length < 6) {
            senhaError.textContent = 'A senha deve ter pelo menos 6 caracteres.';
            isValid = false;
        } else {
            senha.style.borderColor = 'green';
        }

        if (senha.value !== confirmarSenha.value) {
            confirmarSenhaError.textContent = 'As senhas não coincidem.';
            isValid = false;
        } else {
            confirmarSenha.style.borderColor = 'green';
        }

        if (!isValid) {
            event.preventDefault(); // Impede o envio apenas se não for válido
        }
    }

    function toggleComprovanteField() {
        if (condicaoPrioritaria.value !== 'nenhuma') {
            comprovanteField.style.display = 'block';
        } else {
            comprovanteField.style.display = 'none';
        }
    }

    // Adiciona o evento de mudança para o campo de condição prioritária
    condicaoPrioritaria.addEventListener('change', toggleComprovanteField);
    toggleComprovanteField(); // Chama a função ao carregar a página

    var form = document.querySelector('form');
    form.addEventListener('submit', validarFormulario);
});