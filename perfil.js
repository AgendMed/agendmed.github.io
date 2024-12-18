document.addEventListener('DOMContentLoaded', function () {
    const fields = {
        nome: document.getElementById('user-name'),
        nomeCompleto: document.getElementById('user-full-name'),
        nomeEdit: document.getElementById('nome-edit'),
        cartSus: document.getElementById('user-cart-sus'),
        cartSusEdit: document.getElementById('cart-sus-edit'),
        cpf: document.getElementById('user-cpf'),
        telefone: document.getElementById('user-phone'),
        telefoneEdit: document.getElementById('telefone-edit'),
        endereco: document.getElementById('user-address'),
        enderecoEdit: document.getElementById('endereco-edit'),
        email: document.getElementById('user-email'),
        emailEdit: document.getElementById('email-edit'),
    };

    const editBtn = document.getElementById('edit-btn');
    const saveBtn = document.getElementById('save-btn');

    // Função para preencher os campos
    function preencherPerfil(cpf) {
        const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {};

        if (usuarios[cpf]) {
            const usuario = usuarios[cpf];

            // Preencher a visualização
            fields.nome.textContent = usuario.nome || '';
            fields.nomeCompleto.textContent = usuario.nome || '';
            fields.cartSus.textContent = usuario.cartSus || '';
            fields.cpf.textContent = usuario.cpf || '';
            fields.telefone.textContent = usuario.telefone || '';
            fields.endereco.textContent = `${usuario.rua}, ${usuario.bairro}` || '';
            fields.email.textContent = usuario.email || '';

            // Preencher os campos de edição
            fields.nomeEdit.value = usuario.nome || '';
            fields.cartSusEdit.value = usuario.cartSus || '';
            fields.telefoneEdit.value = usuario.telefone || '';
            fields.enderecoEdit.value = `${usuario.rua}, ${usuario.bairro}` || ''; // Agora você salva a rua e o bairro corretamente
            fields.emailEdit.value = usuario.email || '';
        } else {
            Swal.fire({
                title: 'Erro!',
                text: 'Usuário não encontrado.',
                icon: 'error',
                timer: 3000
            });
        }
    }

    // Função para salvar alterações
    function salvarAlteracoes() {
        const cpfUsuarioLogado = localStorage.getItem('cpfLogado');
        
        if (cpfUsuarioLogado) {
            const usuarios = JSON.parse(localStorage.getItem('usuarios')) || {};
            const usuario = usuarios[cpfUsuarioLogado];

            // Atualizar os dados com os novos valores
            usuario.nome = fields.nomeEdit.value;
            usuario.cartSus = fields.cartSusEdit.value;
            usuario.telefone = fields.telefoneEdit.value;
            usuario.email = fields.emailEdit.value;

            // Separar rua e bairro do endereço editado
            const endereco = fields.enderecoEdit.value.split(','); // Separando por vírgula
            usuario.rua = endereco[0]?.trim(); // A rua fica antes da vírgula
            usuario.bairro = endereco[1]?.trim(); // O bairro fica depois da vírgula

            // Salvar no localStorage
            usuarios[cpfUsuarioLogado] = usuario;
            localStorage.setItem('usuarios', JSON.stringify(usuarios));

            Swal.fire({
                title: 'Sucesso!',
                text: 'Perfil atualizado com sucesso.',
                icon: 'success',
                timer: 3000
            });

            // Atualizar os campos de visualização com os novos valores
            fields.nome.textContent = usuario.nome || '';
            fields.cartSus.textContent = usuario.cartSus || '';
            fields.telefone.textContent = usuario.telefone || '';
            fields.endereco.textContent = `${usuario.rua}, ${usuario.bairro}` || '';
            fields.email.textContent = usuario.email || '';

            // Alternar de volta para a visualização
            fields.nome.style.display = 'block';
            fields.cartSus.style.display = 'block';
            fields.telefone.style.display = 'block';
            fields.endereco.style.display = 'block';
            fields.email.style.display = 'block';

            fields.nomeEdit.style.display = 'none';
            fields.cartSusEdit.style.display = 'none';
            fields.telefoneEdit.style.display = 'none';
            fields.enderecoEdit.style.display = 'none';
            fields.emailEdit.style.display = 'none';

            editBtn.style.display = 'block';
            saveBtn.style.display = 'none';
        } else {
            Swal.fire({
                title: 'Erro!',
                text: 'Nenhum usuário logado.',
                icon: 'error',
                timer: 3000
            });
        }
    }

    // Alternar entre visualização e edição
    editBtn.addEventListener('click', function () {
        saveBtn.style.display = 'block';
        editBtn.style.display = 'none';
        
        fields.nome.style.display = 'none';
        fields.cartSus.style.display = 'none';
        fields.telefone.style.display = 'none';
        fields.email.style.display = 'none';
        fields.endereco.style.display = 'none'; // Agora esconderemos o endereço na visualização
        fields.nomeEdit.style.display = 'block';
        fields.cartSusEdit.style.display = 'block';
        fields.telefoneEdit.style.display = 'block';
        fields.enderecoEdit.style.display = 'block'; // Exibir o campo de edição do endereço
        fields.emailEdit.style.display = 'block';
    });

    saveBtn.addEventListener('click', salvarAlteracoes);

    // Preencher os dados do usuário ao carregar a página
    const cpfUsuarioLogado = localStorage.getItem('cpfLogado');
    if (cpfUsuarioLogado) {
        preencherPerfil(cpfUsuarioLogado);
    }
});
