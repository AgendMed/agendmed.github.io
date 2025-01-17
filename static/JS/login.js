const cpfInput = document.getElementById("cpf-login");
const senhaInput = document.getElementById("senha-login");

// Mensagens de erro
const cpfError = document.getElementById("cpf-error");
const senhaError = document.getElementById("senha-error");

function validarCPF(cpf) {
    return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(cpf) && cpf.length === 14; 
}

function validarSenha(senha) {
    return senha.length >= 6;
}

// Mensagens de erro
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
    const submitBtn = document.querySelector('button[type="submit"]');
    submitBtn.disabled = !(cpfValido && senhaValida);
}

// Formatar CPF enquanto digita
function formatarCPF(cpf) {
    cpf = cpf.replace(/\D/g, "");
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