document.getElementById('id_preco_compra').addEventListener('input', function () {
    var precoCompra = parseFloat(this.value);
    var precoVenda = precoCompra * 1.8;  // Cálculo do Preço de Venda
    document.getElementById('preco_venda').textContent = precoVenda.toFixed(2);
});

document.addEventListener('DOMContentLoaded', function () {
    // Altera os labels para 'Usuário:' e 'Senha:'
    document.querySelector("label[for='id_username']").textContent = "Usuário:";
    document.querySelector("label[for='id_password']").textContent = "Senha:";
});


