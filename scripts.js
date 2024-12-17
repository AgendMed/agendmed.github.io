// Scripts de cadastro
document.addEventListener('DOMContentLoaded', function() {
    var nome = document.getElementById('nome');
    var cartSus = document.getElementById('cartSus');
    var cpf = document.getElementById('cpf');
    var dataNascimento = document.getElementById('dataNascimento');
    var telefone = document.getElementById('telefone');
    var bairro = document.getElementById('bairro');
    var rua = document.getElementById('rua');
    var email = document.getElementById('emailCadastro');
    var senha = document.getElementById('senhaCadastro');
    var confirmarSenha = document.getElementById('confirmarSenha');

    var nomeError = document.getElementById('nomeError');
    var cartSusError = document.getElementById('cartSusError');
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
        event.preventDefault();
        
        nomeError.textContent= '';
        cartSusError.textContent= '';
        cpfError.textContent= '';
        dataNascimentoError.textContent= '';
        telefoneError.textContent= '';
        bairroError.textContent= '';
        ruaError.textContent= '';
        emailError.textContent = '';
        senhaError.textContent = '';
        confirmarSenhaError.textContent = '';

        let isValid = true;

        if (nome.value.trim() === '') {
            nomeError.textContent = 'Por favor, preencha o campo Nome.';
            isValid = false;
        }   else {
            nome.style.borderColor = 'green';
        }

        if (cartSus.value.trim() === ''){
            cartSusError.textContent = 'Por favor, preencha o campo Cartão SUS.';
            isValid = false;
        }   else {
            cartSus.style.borderColor = 'green';
        }

        if (!/^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(cpf.value)) {
            cpfError.textContent = 'Por favor, insira um CPF válido (ex: 000.000.000-00.'
            isValid = false;
        }   else {
            cpf.style.borderColor = 'green';
        }
        if (dataNascimento.value === '') {
            dataNascimentoError.textContent = 'Por favor, preencha o campo Data de Nascimento';
            isValid = false;
        }   else {
            dataNascimento.style.borderColor = 'green';
        }

        if (telefone.value.trim() === '') {
            telefoneError.textContent = 'Por favor, preencha o campo Telefone';
            isValid = false;
        }   else {
            telefone.style.borderColor = 'green';
        }

        if (bairro.value.trim() === '') {
            bairroError.textContent = 'Por favor, preencha o campo Bairro';
            isValid = false;
        }   else {
            bairro.style.borderColor = 'green';
        }

        if (rua.value.trim() === '') {
            ruaError.textContent = 'Por favor, preencha o campo Rua';
            isValid = false;
        }   else {
            rua.style.borderColor = 'green';
        }

        if (complemento.value.trim() !== '') {
            complemento.style.borderColor = 'green';
        }

        if (grupoPrioritario.checked) {
            grupoPrioritario.style.borderColor = 'green';
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
                cartSus: cartSus.value,
                cpf: cpf.value,
                dataNascimento: dataNascimento.value,
                telefone: telefone.value,
                bairro: bairro.value,
                rua: rua.value,
                complemento: complemento.value,
                grupoPrioritario: grupoPrioritario.checked,
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
            cartSus.value = '';
            cpf.value = '';
            dataNascimento.value = '';
            telefone.value = '';
            bairro.value = '';
            rua.value = '';
            complemento.value = '';
            grupoPrioritario.checked = false;
            email.value = '';
            senha.value = '';
            confirmarSenha.value = '';
        }
    }

    var form = document.querySelector('form');
    form.addEventListener('submit', validarFormulario);
});

// Scripts de login
document.addEventListener('DOMContentLoaded', function() {
    const cpfInput = document.getElementById("cpf-login");
    const senhaInput = document.getElementById("senha-login");
    const submitBtn = document.getElementById("submit-btn");

    // Mensagens de erro
    const cpfError = document.getElementById("cpf-error");
    const senhaError = document.getElementById("senha-error");

    // Valida CPF (formato 000.000.000-00)
    function validarCPF(cpf) {
        return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(cpf) && cpf.length === 14; // Verifica se o CPF tem 14 caracteres
    }

    // Valida Senha (mínimo 6 caracteres)
    function validarSenha(senha) {
        return senha.length >= 6;
    }

    // Exibir ou ocultar erro
    function validarCampo(input, errorMsg, isValid) {
        if (isValid) {
            input.classList.remove("error");
            errorMsg.textContent = "";
        } else {
            input.classList.add("error");
            errorMsg.textContent = isValid ? "" : errorMsg.textContent;
        }
    }

    // Habilitar ou desabilitar o botão
    function atualizarBotaoSubmit() {
        const cpfValido = validarCPF(cpfInput.value);
        const senhaValida = validarSenha(senhaInput.value);

        submitBtn.disabled = !(cpfValido && senhaValida);
    }

    // Formatar CPF enquanto o usuário digita
    function formatarCPF(cpf) {
        cpf = cpf.replace(/\D/g, ""); // Remove tudo o que não é número
        if (cpf.length <= 11) {
            cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
            cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
            cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
        } else {
            cpf = cpf.substring(0, 11); // Garante que não passe de 11 dígitos numéricos
        }
        return cpf;
    }

    // Eventos em tempo real para CPF
    cpfInput.addEventListener("input", () => {
        cpfInput.value = formatarCPF(cpfInput.value); // Formatar CPF enquanto digita
        const valido = validarCPF(cpfInput.value);
        validarCampo(cpfInput, cpfError, valido);
        cpfError.textContent = valido ? "" : "CPF inválido (formato: 000.000.000-00)";
        atualizarBotaoSubmit();
    });

    // Eventos em tempo real para Senha
    senhaInput.addEventListener("input", () => {
        const valido = validarSenha(senhaInput.value);
        validarCampo(senhaInput, senhaError, valido);
        senhaError.textContent = valido ? "" : "A senha deve ter pelo menos 6 caracteres";
        atualizarBotaoSubmit();
    });
});
