from django.shortcuts import render, redirect, get_object_or_404
from .models import Venda, ItemVenda
from cadastros.models import Produto
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
from decimal import Decimal
from django.utils import timezone
from django.contrib import messages
from cadastros.forms import ProdutoForm

@login_required
def nota_fiscal(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)
    itens = ItemVenda.objects.filter(venda=venda)
    
    # Calcular o total para cada item e adicionar como um atributo temporário
    for item in itens:
        item.total_item = item.preco_unitario * item.quantidade

    return render(request, 'nota_fiscal.html', {'venda': venda, 'itens': itens})

@login_required
def buscar_produto(request):
    termo_busca = request.GET.get('termo')
    if termo_busca:
        produtos = Produto.objects.filter(
            (Q(nome__icontains=termo_busca) | Q(codigo_barras__icontains=termo_busca)) &
            Q(usuario=request.user)
        )
        return JsonResponse({'produtos': list(produtos.values('id', 'nome', 'codigo_barras', 'preco_venda'))})
    return JsonResponse({'produtos': []})



@login_required
def iniciar_venda(request):
    venda = Venda.objects.create(usuario=request.user)
    return redirect('adicionar_produto', venda_id=venda.id)



@login_required
def adicionar_produto(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)

    # Verifica se o usuário da venda é o mesmo que está logado
    if venda.usuario != request.user:
        messages.error(request, "Você não tem permissão para modificar esta venda.")
        return redirect('alguma_url_para_redirecionar')

    if request.method == 'POST':
        if 'produto_id' in request.POST:
            produto_id = request.POST.get('produto_id')
            quantidade = int(request.POST.get('quantidade'))

            try:
                # Verifica se o produto pertence ao usuário logado antes de adicionar
                produto = Produto.objects.get(id=produto_id, usuario=request.user)
                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco_venda
                )
                venda.total += produto.preco_venda * quantidade
                venda.save()
            except Produto.DoesNotExist:
                messages.error(request, "Produto não encontrado ou você não tem permissão para adicioná-lo.")

        elif 'desconto' in request.POST:
            desconto = Decimal(request.POST.get('desconto', '0'))
            venda.desconto = desconto
            venda.total_com_desconto = venda.total - (venda.total * desconto / Decimal('100'))
            venda.save()

    # Filtra produtos pelo usuário logado
    produtos = Produto.objects.filter(usuario=request.user)

    return render(request, 'adicionar_produto.html', {
        'venda': venda,
        'produtos': produtos,
        'desconto': venda.desconto,
        'total_com_desconto': venda.total_com_desconto
    })

@login_required
def finalizar_venda(request, venda_id):
    venda = Venda.objects.get(id=venda_id)
    venda.total = venda.aplicar_desconto()
    venda.save()
    return redirect('nota_fiscal', venda_id=venda.id)

@login_required
def get_total_venda(request, venda_id):
    venda = Venda.objects.get(id=venda_id)
    total = sum(item.produto.preco * item.quantidade for item in venda.itens.all())
    return JsonResponse({'total': total})

@login_required
def listar_vendas(request):
    vendas = Venda.objects.all()
    vendas = Venda.objects.filter(usuario=request.user)
    return render(request, 'listar_vendas.html', {'vendas': vendas})


@login_required
def vendas_do_dia(request):
    data_atual = timezone.now().date()
    vendas = Venda.objects.filter(data_hora__date=data_atual, usuario=request.user)
    return render(request, 'vendas_do_dia.html', {'vendas': vendas})

@login_required
def remover_produto(request, venda_id, item_id):
    venda = get_object_or_404(Venda, id=venda_id)

    # Verifica se o usuário da venda é o mesmo que está logado
    if venda.usuario != request.user:
        messages.error(request, "Você não tem permissão para modificar esta venda.")
        return redirect('adicionar_produto', venda_id=venda.id)

    item = get_object_or_404(ItemVenda, id=item_id, venda=venda)

    # Atualiza o total da venda antes de deletar
    venda.total -= item.preco_unitario * item.quantidade
    venda.total_com_desconto = venda.total - (venda.total * venda.desconto / Decimal('100'))
    venda.save()

    item.delete()
    return redirect('adicionar_produto', venda_id=venda.id)


from .forms import ProdutoForm

def cadastrar_produto_ajax(request):
    if request.method == "POST":
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            usuario = request.user
            produto_existente = Produto.objects.filter(nome=nome, usuario=usuario).first()

            if produto_existente:
                # Atualiza produto existente
                produto_existente.codigo_barras = form.cleaned_data['codigo_barras']
                produto_existente.preco_compra = form.cleaned_data['preco_compra']
                produto_existente.preco_venda = form.cleaned_data['preco_venda']  # ✅ Adicionado
                produto_existente.save()
                return JsonResponse({
                    "status": "atualizado",
                    "mensagem": f"Produto '{produto_existente.nome}' atualizado com sucesso.",
                    "produto_id": produto_existente.id,
                    "nome": produto_existente.nome
                })
            else:
                # Cria novo produto
                produto = Produto.objects.create(
                    usuario=usuario,
                    nome=nome,
                    codigo_barras=form.cleaned_data['codigo_barras'],
                    preco_compra=form.cleaned_data['preco_compra'],
                    preco_venda=form.cleaned_data['preco_venda']  # ✅ Adicionado
                )
                return JsonResponse({
                    "status": "cadastrado",
                    "mensagem": f"Produto '{produto.nome}' cadastrado com sucesso.",
                    "produto_id": produto.id,
                    "nome": produto.nome
                })
        else:
            return JsonResponse({"status": "erro", "erros": form.errors})
    return JsonResponse({"status": "erro", "erros": "Método inválido"})

@login_required
def adicionar_produto(request, venda_id):
    venda = get_object_or_404(Venda, id=venda_id)

    if venda.usuario != request.user:
        messages.error(request, "Você não tem permissão para modificar esta venda.")
        return redirect('alguma_url_para_redirecionar')

    if request.method == 'POST':
        if 'produto_id' in request.POST:
            produto_id = request.POST.get('produto_id')
            quantidade = int(request.POST.get('quantidade'))

            try:
                produto = Produto.objects.get(id=produto_id, usuario=request.user)
                ItemVenda.objects.create(
                    venda=venda,
                    produto=produto,
                    quantidade=quantidade,
                    preco_unitario=produto.preco_venda
                )
                venda.total += produto.preco_venda * quantidade
                venda.save()
            except Produto.DoesNotExist:
                messages.error(request, "Produto não encontrado ou você não tem permissão para adicioná-lo.")

        elif 'desconto' in request.POST:
            desconto = Decimal(request.POST.get('desconto', '0'))
            venda.desconto = desconto
            venda.total_com_desconto = venda.total - (venda.total * desconto / Decimal('100'))
            venda.save()

    produtos = Produto.objects.filter(usuario=request.user)
    form = ProdutoForm()  # <--- FORM PARA O MODAL

    return render(request, 'adicionar_produto.html', {
        'venda': venda,
        'produtos': produtos,
        'desconto': venda.desconto,
        'total_com_desconto': venda.total_com_desconto,
        'form': form,  # <--- ENVIA PARA O TEMPLATE
    })
