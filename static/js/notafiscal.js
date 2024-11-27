function confirmarFinalizacao(vendaId) {
    const querImprimir = confirm("Deseja imprimir a nota fiscal?");
    // Enviar resposta para o backend
    fetch(`/caminho/para/finalizar/venda/${vendaId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'), // Função para pegar o CSRF token
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ imprimirNota: querImprimir })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            if (querImprimir) {
                // Lógica para impressão. Pode ser abrir uma nova janela com a nota fiscal.
                window.open(`/caminho/para/nota/fiscal/${vendaId}/`, '_blank');
            }
            // Redirecionar para a página de confirmação ou listar vendas
            window.location.href = '/caminho/para/sucesso/';
        }
    }).catch(error => console.error('Error:', error));
}

// Função para obter o CSRFToken
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