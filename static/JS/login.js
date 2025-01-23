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


cpfInput.addEventListener("input", () => {
    cpfInput.value = formatarCPF(cpfInput.value); // Formatar CPF enquanto digita
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

document.addEventListener("DOMContentLoaded", function() {
    const cpfInput = document.getElementById("cpf-login");
    const senhaInput = document.getElementById("senha-login");
    const submitBtn = document.getElementById("submit-btn");

    function validateForm() {
        if (cpfInput.value && senhaInput.value.length >= 6) {
            submitBtn.disabled = false;
        } else {
            submitBtn.disabled = true;
        }
    }

    cpfInput.addEventListener("input", validateForm);
    senhaInput.addEventListener("input", validateForm);
});

