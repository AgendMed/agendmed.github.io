document.addEventListener('DOMContentLoaded', function () {
    const fields = {
        nome: document.getElementById('user-name'),
        nomeCompleto: document.getElementById('user-full-name'), // Campo do nome completo
        cartSus: document.getElementById('user-cart-sus'),
        cpf: document.getElementById('user-cpf'),
        telefone: document.getElementById('user-phone'),
        endereco: document.getElementById('user-address'),
        email: document.getElementById('user-email')
    };

    function preencherPerfil(cpf) {
        const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {};

        if (usuarios[cpf]) {
            const usuario = usuarios[cpf];
            
            fields.nome.textContent = usuario.nome || '';
            fields.nomeCompleto.textContent = usuario.nome || '';
            fields.cartSus.textContent = usuario.cartSus || '';
            fields.cpf.textContent = usuario.cpf || '';
            fields.telefone.textContent = usuario.telefone || '';
            fields.endereco.textContent = `${usuario.rua}, ${usuario.bairro}` || '';
            fields.email.textContent = usuario.email || '';
        } else {
            Swal.fire({
                title: 'Erro!',
                text: 'Usuário não encontrado.',
                icon: 'error',
                timer: 3000
            });
        }
    }

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
