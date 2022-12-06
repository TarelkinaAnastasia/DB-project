from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from shop.models import Product

def order_create(request):
    cart = Cart(request)
    #print("req  ", request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
                # item.stock = item.stock - item.quantiti
                product_in_db = Product.objects.get(id=item['product'].id)
                new_stock = product_in_db.stock - item['quantity'] if product_in_db.stock - item['quantity'] >= 0 else 0
                product_queryset = Product.objects.filter(id=item['product'].id)
                product_queryset.update(stock=new_stock)
                if new_stock == 0:
                    product_queryset.update(available=False)

            # очистка корзины
            cart.clear()
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html',
                          {'order': order})

    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
# Create your views here.
