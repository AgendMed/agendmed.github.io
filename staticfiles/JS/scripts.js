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