const cpfInput = document.getElementById("cpf-login");
const senhaInput = document.getElementById("senha-login");
<<<<<<< HEAD
=======
const submitBtn = document.getElementById("submit-btn");
>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54

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

<<<<<<< HEAD
<<<<<<<< HEAD:static/JS/login.js
// Mensagens de erro
========
// Exibir ou ocultar erro
>>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54:staticfiles/JS/login.js
=======
// Exibir ou ocultar erro
>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
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
<<<<<<< HEAD
<<<<<<<< HEAD:static/JS/login.js
    const submitBtn = document.querySelector('button[type="submit"]');
========

>>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54:staticfiles/JS/login.js
=======

>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
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

<<<<<<< HEAD
// Eventos em tempo real
=======

>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
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
<<<<<<< HEAD
<<<<<<<< HEAD:static/JS/login.js
});
========
});
>>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54:staticfiles/JS/login.js
=======
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

>>>>>>> 3051aee9c0858b89d2513a603c47cd992e1a3a54
