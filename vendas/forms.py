from django import forms
from .models import Produto

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'tipo', 'codigo_barras', 'preco_compra', 'preco_venda', 'porcentagem_lucro', 'imagem']
