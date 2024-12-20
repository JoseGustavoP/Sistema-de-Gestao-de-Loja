from django.urls import path
from . import views

urlpatterns = [
    path('iniciar_venda/', views.iniciar_venda, name='iniciar_venda'),
    path('adicionar_produto/<int:venda_id>/', views.adicionar_produto, name='adicionar_produto'),
    path('finalizar_venda/<int:venda_id>/', views.finalizar_venda, name='finalizar_venda'),
    path('buscar_produto/', views.buscar_produto, name='buscar_produto'),
    path('get_total_venda/<int:venda_id>/', views.get_total_venda, name='get_total_venda'),
    path('vendas/', views.listar_vendas, name='listar_vendas'),
    path('vendas_do_dia/', views.vendas_do_dia, name='vendas_do_dia'),
    path('nota_fiscal/<int:venda_id>/', views.nota_fiscal, name='nota_fiscal'),

]