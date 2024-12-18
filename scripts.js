document.addEventListener('DOMContentLoaded', function () {
    // Seleção de elementos
    const form = document.querySelector('form');
    const fields = {
        nome: document.getElementById('nome'),
        cartSus: document.getElementById('cartSus'),
        cpf: document.getElementById('cpf'),
        dataNascimento: document.getElementById('dataNascimento'),
        telefone: document.getElementById('telefone'),
        bairro: document.getElementById('bairro'),
        rua: document.getElementById('rua'),
        complemento: document.getElementById('complemento'),
        grupoPrioritario: document.getElementById('grupoPrioritario'),
        email: document.getElementById('emailCadastro'),
        senha: document.getElementById('senhaCadastro'),
        confirmarSenha: document.getElementById('confirmarSenha')
    };

    const errorMessages = {
        nomeError: document.getElementById('nomeError'),
        cartSusError: document.getElementById('cartSusError'),
        cpfError: document.getElementById('cpfError'),
        dataNascimentoError: document.getElementById('dataNascimentoError'),
        telefoneError: document.getElementById('telefoneError'),
        bairroError: document.getElementById('bairroError'),
        ruaError: document.getElementById('ruaError'),
        emailError: document.getElementById('emailError'),
        senhaError: document.getElementById('senhaError'),
        confirmarSenhaError: document.getElementById('confirmarSenhaError')
    };

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Função para aplicar máscara ao CPF
    function aplicarMascaraCPF(cpf) {
        return cpf.replace(/\D/g, '')
                  .replace(/(\d{3})(\d)/, '$1.$2')
                  .replace(/(\d{3})(\d)/, '$1.$2')
                  .replace(/(\d{3})(\d{2})$/, '$1-$2');
    }

    // Função para aplicar máscara ao telefone
    function aplicarMascaraTelefone(telefone) {
        return telefone.replace(/\D/g, '')
                       .replace(/(\d{2})(\d)/, '($1) $2')
                       .replace(/(\d)(\d{4})$/, '$1-$2');
    }

    // Função de validação
    function validarCampo(campo, errorElement, validationFn) {
        const value = campo.value.trim();
        errorElement.textContent = '';
        campo.style.borderColor = '';

        if (!validationFn(value)) {
            errorElement.textContent = `Por favor, preencha o campo ${campo.name}.`;
            campo.style.borderColor = 'red';
            return false;
        } else {
            campo.style.borderColor = 'green';
            return true;
        }
    }

    // Funções de validação específicas
    function validarNome(value) {
        return value !== '';
    }

    function validarCartaoSus(value) {
        return value !== ''; 
    }

    function validarCPF(value) {
        return /^\d{3}\.\d{3}\.\d{3}-\d{2}$/.test(value);
    }

    function validarDataNascimento(value) {
        return value !== '';
    }

    function validarTelefone(value) {
        return value !== '';
    }

    function validarBairro(value) {
        return value !== '';
    }

    function validarRua(value) {
        return value !== '';
    }

    function validarEmail(value) {
        return emailRegex.test(value);
    }

    function validarSenha(value) {
        return value.length >= 6;
    }

    function validarConfirmarSenha(value) {
        return value === fields.senha.value;
    }

    // Validação em tempo real
    Object.keys(fields).forEach(key => {
        fields[key].addEventListener('input', function () {
            switch (key) {
                case 'complemento': // Ignorar
                    break;
                case 'cartSus':
                    validarCampo(fields.cartSus, errorMessages.cartSusError, validarCartaoSus);
                    break;
                case 'cpf':
                    fields.cpf.value = aplicarMascaraCPF(fields.cpf.value);
                    validarCampo(fields.cpf, errorMessages.cpfError, validarCPF);
                    break;
                case 'telefone':
                    fields.telefone.value = aplicarMascaraTelefone(fields.telefone.value);
                    validarCampo(fields.telefone, errorMessages.telefoneError, validarTelefone);
                    break;
                case 'email':
                    validarCampo(fields.email, errorMessages.emailError, validarEmail);
                    break;
                case 'senha':
                    validarCampo(fields.senha, errorMessages.senhaError, validarSenha);
                    break;
                case 'confirmarSenha':
                    validarCampo(fields.confirmarSenha, errorMessages.confirmarSenhaError, validarConfirmarSenha);
                    break;
                default:
                    const validateFn = window[`validar${key.charAt(0).toUpperCase() + key.slice(1)}`];
                    if (typeof validateFn === 'function') {
                        validarCampo(fields[key], errorMessages[`${key}Error`], validateFn);
                    }
                    break;
            }
        });
    });

    // Função de validação do formulário
    function validarFormulario(event) {
        event.preventDefault();
        
        let isValid = true;

        Object.keys(fields).forEach(key => {
            switch (key) {
                case 'complemento': // Ignore este campo
                    break;
                case 'cartSus':
                    isValid &= validarCampo(fields.cartSus, errorMessages.cartSusError, validarCartaoSus);
                    break;
                case 'cpf':
                    isValid &= validarCampo(fields.cpf, errorMessages.cpfError, validarCPF);
                    break;
                case 'telefone':
                    isValid &= validarCampo(fields.telefone, errorMessages.telefoneError, validarTelefone);
                    break;
                case 'email':
                    isValid &= validarCampo(fields.email, errorMessages.emailError, validarEmail);
                    break;
                case 'senha':
                    isValid &= validarCampo(fields.senha, errorMessages.senhaError, validarSenha);
                    break;
                case 'confirmarSenha':
                    isValid &= validarCampo(fields.confirmarSenha, errorMessages.confirmarSenhaError, validarConfirmarSenha);
                    break;
                default:
                    const validateFn = window[`validar${key.charAt(0).toUpperCase() + key.slice(1)}`];
                    if (typeof validateFn === 'function') {
                        isValid &= validarCampo(fields[key], errorMessages[`${key}Error`], validateFn);
                    }
                    break;
            }
        });

        if (isValid) {
            const usuario = {
                nome: fields.nome.value,
                cartSus: fields.cartSus.value,
                cpf: fields.cpf.value,
                dataNascimento: fields.dataNascimento.value,
                telefone: fields.telefone.value,
                bairro: fields.bairro.value,
                rua: fields.rua.value,
                complemento: fields.complemento.value,
                grupoPrioritario: fields.grupoPrioritario.checked,
                email: fields.email.value,
                senha: fields.senha.value
            };

            // Recuperar a lista de usuários do localStorage
            const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {};

            // Adicionar o novo usuário usando o CPF como chave
            usuarios[usuario.cpf] = usuario;

            // Salvar a lista atualizada de usuários no localStorage
            localStorage.setItem('usuarios', JSON.stringify(usuarios));

            Swal.fire({
                title: 'Cadastro realizado!',
                text: 'Seus dados foram salvos com sucesso.',
                icon: 'success',
                timer: 3000
            });

            // Limpar campos após o cadastro
            Object.values(fields).forEach(field => {
                field.value = '';
                field.style.borderColor = '';
            });
            fields.grupoPrioritario.checked = false;
        }
    }

    form.addEventListener('submit', validarFormulario);
});
