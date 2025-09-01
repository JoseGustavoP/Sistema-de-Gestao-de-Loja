from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

class Produto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    tipo = models.CharField(max_length=100, blank=True, null=True)
    codigo_barras = models.CharField(max_length=100, blank=True, null=True)

    # Preço de compra agora é opcional
    preco_compra = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Lucro padrão
    porcentagem_lucro = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Agora o usuário pode definir manualmente
    preco_venda = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    imagem = models.ImageField(upload_to='static/img/imagens_produtos', blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Regra:
        - Se preco_venda já foi informado manualmente, mantém.
        - Se não houver preco_venda mas tiver preco_compra + porcentagem_lucro, calcula.
        """
        if not self.preco_venda:  
            if self.preco_compra and self.porcentagem_lucro:
                lucro = Decimal(self.porcentagem_lucro) / Decimal('100.0')
                self.preco_venda = self.preco_compra * (Decimal('1.0') + lucro)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome
