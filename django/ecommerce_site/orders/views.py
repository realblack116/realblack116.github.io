from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from products.models import Product
from .cart import Cart
from django.views.decorators.csrf import csrf_exempt

def add_to_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product_id)
    return redirect('cart_view')

def cart_view(request):
    cart = Cart(request)
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.get_items():
        product = get_object_or_404(Product, id=product_id)
        item_total = quantity * product.price
        total_price += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': item_total
        })

    context = {
        'cart_items': cart_items,
        'cart_total': total_price
    }
    return render(request, 'orders/cart.html', context)

def remove_from_cart(request, product_id):
    cart = Cart(request)
    cart.remove(product_id)
    return redirect('cart_view')

@csrf_exempt
def create_order(request):
    cart = Cart(request)

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        order = Order.objects.create(name=name, email=email)

        for product_id, quantity in cart.get_items():
            product = Product.objects.filter(id=int(product_id)).first()
            if product:
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

        cart.clear()
        return redirect('order_success')

    return render(request, 'orders/create_order.html')

def order_success(request):
    return render(request, 'orders/order_success.html')
