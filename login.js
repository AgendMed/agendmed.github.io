const cpfInput = document.getElementById("cpf-login");
const senhaInput = document.getElementById("senha-login");
const submitBtn = document.getElementById("submit-btn");

// Mensagens de erro
const cpfError = document.getElementById("cpf-error");
const senhaError = document.getElementById("senha-error");

function validarCPF(cpf) {
    return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(cpf) && cpf.length === 14; 
}

function validarSenha(senha) {
    return senha.length >= 6;
}

//mensagens de erro
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

// Formatar CPF enquanto digita
function formatarCPF(cpf) {
    cpf = cpf.replace(/\D/g, ""); // Remove tudo que não é número
    if (cpf.length <= 11) {
        cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
        cpf = cpf.replace(/(\d{3})(\d)/, "$1.$2");
        cpf = cpf.replace(/(\d{3})(\d{1,2})$/, "$1-$2");
    } else {
        cpf = cpf.substring(0, 11);
    }
    return cpf;
}

cpfInput.addEventListener("input", () => {
    cpfInput.value = formatarCPF(cpfInput.value);
    const valido = validarCPF(cpfInput.value);
    validarCampo(cpfInput, cpfError, valido);
    cpfError.textContent = valido ? "" : "CPF inválido (formato: 000.000.000-00)";
    atualizarBotaoSubmit();
});

senhaInput.addEventListener("input", () => {
    const valido = validarSenha(senhaInput.value);
    validarCampo(senhaInput, senhaError, valido);
    senhaError.textContent = valido ? "" : "A senha deve ter pelo menos 6 caracteres";
    atualizarBotaoSubmit();
});

// Função para realizar o login
function realizarLogin(event) {
    event.preventDefault();

    const cpf = cpfInput.value;
    const senha = senhaInput.value.trim();

    const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {}; 

    // Verificar se o CPF existe e se a senha está correta
    if (usuarios[cpf] && usuarios[cpf].senha === senha) {
        localStorage.setItem('cpfLogado', cpf);
        window.location.href = 'user.html';
    } else {
        alert('CPF ou senha inválidos!');
    }
}

// Associar a função de login ao evento de envio do formulário
const formLogin = document.querySelector('form');
formLogin.addEventListener('submit', realizarLogin);
