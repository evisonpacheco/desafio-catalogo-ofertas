from django.shortcuts import render
from ofertas.models import Product 

def products_list(request):
    # Filtros
    products = Product.objects.all()

    # Filtro por Frete Grátis (Free Shipping)
    if request.GET.get('free_shipping'):
        products = products.filter(free_shipping=True)

    # Filtro por Entrega Full (Full Delivery)
    if request.GET.get('full'):
        products = products.filter(delivery_type__icontains='Full')

    # Ordenação (Sorting)
    sorting = request.GET.get('sorting')
    if sorting == 'highest_price':
        products = products.order_by('-price')
    elif sorting == 'lowest_price':
        products = products.order_by('price')
    elif sorting == 'highest_discount':
        products = products.order_by('-discount_percentage')

    # Extra: Produtos com maior preço, menor preço e maior desconto
    highest_price = products.order_by('-price').first()
    lowest_price = products.order_by('price').first()
    highest_discount = products.order_by('-discount_percentage').first()

    # Passa os produtos e os extras para o template
    context = {
        'products': products,
        'highest_price': highest_price,
        'lowest_price': lowest_price,
        'highest_discount': highest_discount,
    }

    return render(request, 'ofertas/products_list.html', context)