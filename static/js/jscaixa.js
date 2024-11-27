document.addEventListener('DOMContentLoaded', function () {
    const buscaCodigoBarras = document.getElementById('buscaCodigoBarras');
    const listaProdutos = document.getElementById('listaProdutos');
    const opcoesOriginais = Array.from(listaProdutos.options);

    buscaCodigoBarras.addEventListener('input', function () {
        const termoBusca = buscaCodigoBarras.value.toLowerCase();
        filtrarOpcoesPorCodigoBarras(termoBusca);
    });

    function filtrarOpcoesPorCodigoBarras(termoBusca) {
        listaProdutos.innerHTML = '';
        const opcoesFiltradas = opcoesOriginais.filter(opcao => {
            const codigoBarras = opcao.getAttribute('data-codigo-barras');
            return codigoBarras.toLowerCase().includes(termoBusca);
        });
        opcoesFiltradas.forEach(opcao => listaProdutos.appendChild(opcao.cloneNode(true)));
    }
});


document.addEventListener('DOMContentLoaded', function () {
    const buscaProduto = document.getElementById('buscaProduto');
    const listaProdutos = document.getElementById('listaProdutos');
    const opcoesOriginais = Array.from(listaProdutos.options);

    buscaProduto.addEventListener('input', function () {
        const termoBusca = buscaProduto.value.toLowerCase();
        listaProdutos.innerHTML = '';

        const opcoesFiltradas = opcoesOriginais.filter(opcao =>
            opcao.text.toLowerCase().includes(termoBusca)
        );

        opcoesFiltradas.forEach(opcao => {
            listaProdutos.appendChild(opcao.cloneNode(true));
        });
    });
});

function atualizarTotal(vendaId) {
    fetch(`/caminho_para/get_total_venda/${vendaId}/`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('totalVenda').innerText = 'R$ ' + data.total;
        });
}

function sendPostRequest(url, data) {
    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    }).then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

