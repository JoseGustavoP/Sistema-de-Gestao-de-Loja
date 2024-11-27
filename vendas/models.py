from django.db import models
from django.contrib.auth.models import User
from cadastros.models import Produto


class Venda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    data_hora = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    desconto = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    total_com_desconto = models.FloatField(default=0.0)  # Total após aplicar desconto
    finalizada = models.BooleanField(default=False)


    def aplicar_desconto(self):
        return self.total * (1 - self.desconto / 100)

class ItemVenda(models.Model):
    venda = models.ForeignKey(Venda, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.IntegerField()
    preco_unitario = models.DecimalField(max_digits=7, decimal_places=2)
    