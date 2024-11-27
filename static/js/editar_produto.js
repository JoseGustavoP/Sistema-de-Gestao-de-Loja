$(document).ready(function() {
    $('#updateProdutoForm').on('submit', function(event) {
        event.preventDefault(); // Previne o envio normal do formulário
        var formData = new FormData(this);
        
        $.ajax({
            url: $(this).attr('action'), // Pega a URL do action do formulário
            type: $(this).attr('method'), // Pega o método do formulário (POST)
            data: formData,
            processData: false, // Impede o jQuery de processar os dados
            contentType: false, // Impede o jQuery de definir o contentType
            success: function(data) {
                // Trate o sucesso, como fechar o modal e atualizar a parte da página com os dados do produto
                $('#editModal').modal('hide');
                // Atualize a parte relevante da página aqui. Pode ser necessário recarregar partes da página ou atualizar elementos específicos com jQuery.
            },
            error: function(xhr, errmsg, err) {
                // Trate o caso de erro aqui
                console.log(xhr.status + ": " + xhr.responseText); // Forneça um feedback de erro no console do navegador
            }
        });
    });
});

document.getElementById('searchInput').addEventListener('keyup', function() {
    var query = this.value;
    fetch(`/caminho_para_view_de_pesquisa?q=${query}`) // Substitua '/caminho_para_view_de_pesquisa' pelo caminho real da sua view de pesquisa
        .then(response => response.text())
        .then(html => {
            document.querySelector("tbody").innerHTML = html;
        })
        .catch(error => console.log(error));
});