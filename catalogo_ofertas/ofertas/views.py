from django.shortcuts import render
from ofertas.models import Produto

def lista_produtos(request):
    # Filtros
    produtos = Produto.objects.all()

    # Filtro por Frete Grátis
    if request.GET.get('frete_gratis'):
        produtos = produtos.filter(frete_gratis=True)

    # Filtro por Entrega Full
    if request.GET.get('full'):
        produtos = produtos.filter(tipo_entrega__icontains='Full')

    # Ordenação
    ordenacao = request.GET.get('ordenacao')
    if ordenacao == 'maior_preco':
        produtos = produtos.order_by('-preco')
    elif ordenacao == 'menor_preco':
        produtos = produtos.order_by('preco')
    elif ordenacao == 'maior_desconto':
        produtos = produtos.order_by('-percentual_desconto')

    # Extra: Produtos com maior preço, menor preço e maior desconto
    maior_preco = produtos.order_by('-preco').first()
    menor_preco = produtos.order_by('preco').first()
    maior_desconto = produtos.order_by('-percentual_desconto').first()

    # Passa os produtos e os extras para o template
    context = {
        'produtos': produtos,
        'maior_preco': maior_preco,
        'menor_preco': menor_preco,
        'maior_desconto': maior_desconto,
    }

    return render(request, 'ofertas/lista_produtos.html', context)