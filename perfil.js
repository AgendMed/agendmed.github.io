document.addEventListener('DOMContentLoaded', function () {
    // Seleção de elementos de perfil
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
        email: document.getElementById('email'),
        senha: document.getElementById('senha')
    };

    // Função para preencher os campos com as informações do usuário
    function preencherPerfil(cpf) {
        const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {};

        if (usuarios[cpf]) {
            const usuario = usuarios[cpf];
            
            // Preenchendo os campos com os dados do usuário
            fields.nome.value = usuario.nome || '';
            fields.cartSus.value = usuario.cartSus || '';
            fields.cpf.value = usuario.cpf || '';
            fields.dataNascimento.value = usuario.dataNascimento || '';
            fields.telefone.value = usuario.telefone || '';
            fields.bairro.value = usuario.bairro || '';
            fields.rua.value = usuario.rua || '';
            fields.complemento.value = usuario.complemento || '';
            fields.grupoPrioritario.checked = usuario.grupoPrioritario || false;
            fields.email.value = usuario.email || '';
            fields.senha.value = usuario.senha || '';
        } else {
            Swal.fire({
                title: 'Erro!',
                text: 'Usuário não encontrado.',
                icon: 'error',
                timer: 3000
            });
        }
    }

    // Recuperar o CPF do usuário logado
    const cpfUsuarioLogado = localStorage.getItem('cpfLogado');

    if (cpfUsuarioLogado) {
        preencherPerfil(cpfUsuarioLogado);
    } else {
        Swal.fire({
            title: 'Erro!',
            text: 'Nenhum usuário logado.',
            icon: 'error',
            timer: 3000
        });
    }
});
