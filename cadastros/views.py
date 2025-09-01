from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Produto
from django.contrib.auth.models import User
from django.db.models import Q
from .forms import ProdutoForm, UserRegisterForm, XMLUploadForm
from django.conf import settings
import os
import xml.etree.ElementTree as ET
import logging
from decimal import Decimal  # Adicionado para usar o tipo Decimal

logger = logging.getLogger(__name__)

def importar_produtos_from_xml(caminho_arquivo_xml, usuario):
    try:
        tree = ET.parse(caminho_arquivo_xml)
        root = tree.getroot()

        # Definir o namespace do XML
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}

        for det in root.findall('.//nfe:det', ns):
            produto_data = {}
            prod = det.find('nfe:prod', ns)
            nome = prod.find('nfe:xProd', ns).text
            codigo_barras = prod.find('nfe:cProd', ns).text
            preco_compra = Decimal(prod.find('nfe:vUnCom', ns).text)

            # Verificar se já existe um produto com o mesmo nome
            produto_existente = Produto.objects.filter(nome=nome, usuario=usuario).first()

            # Se existir, atualizar os dados do produto existente
            if produto_existente:
                produto_existente.codigo_barras = codigo_barras
                produto_existente.preco_compra = preco_compra
                produto_existente.save()
                logger.info(f"Produto '{produto_existente.nome}' atualizado com sucesso.")
            else:
                # Caso contrário, criar um novo produto
                produto_data['usuario'] = usuario
                produto_data['nome'] = nome
                produto_data['codigo_barras'] = codigo_barras
                produto_data['preco_compra'] = preco_compra

                # Criar um objeto Produto com os dados extraídos
                produto = Produto(**produto_data)
                produto.save()
                logger.info(f"Produto '{produto.nome}' importado com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao importar produtos do XML: {str(e)}")

def enviar_xml(request):
    if request.method == 'POST':
        form = XMLUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                xml_file = request.FILES['xml_file']
                # Salva o arquivo XML na pasta de mídia
                with open(os.path.join(settings.MEDIA_ROOT, xml_file.name), 'wb') as destination:
                    for chunk in xml_file.chunks():
                        destination.write(chunk)
                # Obtém o usuário logado atualmente
                usuario_logado = request.user
                # Chama a função para importar produtos do XML
                caminho_arquivo_xml = os.path.join(settings.MEDIA_ROOT, xml_file.name)
                logger.info(f"Chamando a função importar_produtos_from_xml com o caminho {caminho_arquivo_xml}")
                importar_produtos_from_xml(caminho_arquivo_xml, usuario_logado)
                messages.success(request, 'Produtos do XML foram importados com sucesso.')
                return redirect('inicio')  # Redireciona para a página inicial ou outra página desejada
            except Exception as e:
                messages.error(request, f"Erro ao enviar o XML: {str(e)}")
    else:
        form = XMLUploadForm()
    return render(request, 'enviar_xml.html', {'form': form})


def is_staff_user(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff_user)
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            if not request.user.is_superuser:
                user.is_staff = False
            user.save()
            return redirect('inicio')
    else:
        form = UserRegisterForm()
    return render(request, 'usuarios/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('inicio')  # Altere para a URL desejada
        else:
            messages.error(request, 'Usuário ou senha inválidos')

    return render(request, 'usuarios/login.html')





@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            usuario = request.user

            # Pega os dados do form manualmente
            nome = form.cleaned_data.get('nome')
            codigo_barras = form.cleaned_data.get('codigo_barras')
            preco_compra = form.cleaned_data.get('preco_compra')  # pode ser None
            preco_venda = form.cleaned_data.get('preco_venda')    # pode ser None
            porcentagem_lucro = form.cleaned_data.get('porcentagem_lucro') or Decimal('80.0')
            imagem = form.cleaned_data.get('imagem')
            tipo = form.cleaned_data.get('tipo')

            # Se preco_venda não for informado, calcula com preco_compra e porcentagem
            if not preco_venda and preco_compra:
                preco_venda = preco_compra * (Decimal('1.0') + porcentagem_lucro / Decimal('100.0'))

            # Verificar se já existe um produto com o mesmo nome do usuário
            produto_existente = Produto.objects.filter(nome=nome, usuario=usuario).first()

            if produto_existente:
                # Atualiza o produto existente manualmente
                produto_existente.codigo_barras = codigo_barras
                produto_existente.preco_compra = preco_compra
                produto_existente.preco_venda = preco_venda
                produto_existente.porcentagem_lucro = porcentagem_lucro
                produto_existente.tipo = tipo
                if imagem:
                    produto_existente.imagem = imagem
                produto_existente.save()
                messages.success(request, f"Produto '{produto_existente.nome}' atualizado com sucesso.")
            else:
                # Cria um novo produto manualmente
                produto = Produto(
                    usuario=usuario,
                    nome=nome,
                    codigo_barras=codigo_barras,
                    preco_compra=preco_compra,
                    preco_venda=preco_venda,
                    porcentagem_lucro=porcentagem_lucro,
                    tipo=tipo,
                    imagem=imagem
                )
                produto.save()
                messages.success(request, f"Produto '{produto.nome}' cadastrado com sucesso.")

            # Redireciona de acordo com venda_id, se houver
            venda_id = request.POST.get('venda_id')
            if venda_id:
                return redirect('adicionar_produto', venda_id=venda_id)

            return redirect('listar_produtos')
    else:
        form = ProdutoForm()

    return render(request, 'cadastrar_produto.html', {'form': form})

@user_passes_test(is_staff_user)
def listar_usuarios(request):
    usuarios = User.objects.all()
    return render(request, 'usuarios/listar_usuarios.html', {'usuarios': usuarios})

@user_passes_test(is_staff_user)
def delete_usuario(request, user_id):
    if request.user.is_superuser or request.user.is_staff:
        user = get_object_or_404(User, pk=user_id)
        user.delete()
        messages.success(request, "Usuário excluído com sucesso.")
    else:
        messages.error(request, "Você não tem permissão para excluir usuários.")
    return redirect('listar_usuarios')

@login_required
def listar_produtos(request):
    query = request.GET.get('q', '')  # Obter a consulta de pesquisa, ou uma string vazia se não houver consulta
    usuario = request.user  # Obter o usuário atualmente logado
    produtos = Produto.objects.filter(
        usuario=usuario,
        nome__icontains=query
    ) | Produto.objects.filter(
        usuario=usuario,
        codigo_barras__icontains=query
    )
    print(produtos)  # Adicione esta linha para imprimir os produtos filtrados no console do servidor
    return render(request, 'listar_produtos.html', {'produtos': produtos})

@login_required
def delete_produto(request, id):
    produto = Produto.objects.get(id=id)
    produto.delete()
    return redirect('listar_produtos')

@login_required
def update_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        # request.FILES é necessário apenas se o formulário incluir um upload de arquivo,
        # mas a ausência de um novo arquivo aqui não afetará a imagem existente.
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
        # Se o formulário não for válido, renderiza novamente o formulário com os erros.
    else:
        # Carrega o formulário com os dados existentes do produto, incluindo a imagem atual.
        form = ProdutoForm(instance=produto)

    # Este return atende tanto ao caso do formulário inválido quanto ao método GET.
    return render(request, 'editar_produto.html', {'form': form})
