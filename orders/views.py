from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from shop.models import Product
from django.db import IntegrityError, transaction
from functools import partial


def order_create(request):
    cart = Cart(request)
    err_code = None
    order = None
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        try:
            with transaction.atomic():
                if form.is_valid():
                    if len(cart) > 0:
                        for item in cart:
                            product_in_db = Product.objects.select_for_update().get(id=item['product'].id)
                            new_stock = product_in_db.stock - item['quantity']
                            # product_queryset = Product.objects.filter(id=item['product'].id)
                            if new_stock > 0:
                                product_in_db.stock = new_stock
                            elif new_stock == 0:
                                product_in_db.stock = new_stock
                                product_in_db.available = False
                            elif new_stock < 0:
                                err_code = -1
                            product_in_db.save()
                    else:
                        err_code = -2
                    if err_code is None:
                        order = form.save()
                        for item in cart:
                            OrderItem.objects.create(order=order,
                                                    product=item['product'],
                                                    price=item['price'],
                                                    quantity=item['quantity'])

                    # очистка корзины
                    cart.clear()
        except IntegrityError:
            transaction.rollback()
            err_code = -3
        if err_code is None:
            transaction.on_commit(partial(order_created.delay, order.id))
        return render(request, 'orders/order/created.html',
                      {'order': order, 'err_code': err_code})

    else:
        form = OrderCreateForm
    return render(request, 'orders/order/create.html',
                  {'cart': cart, 'form': form})
# Create your views here.
