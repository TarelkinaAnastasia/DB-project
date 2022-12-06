from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from mptt.models import MPTTModel, TreeForeignKey


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        if category.level == 0:
            subcategories = categories.filter(parent_id=category.id)
            products = products.filter(category__in=subcategories)
        else:
            products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def parents_list(request, parent_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True, category = parent_slug )
    if parent_slug:
        category = get_object_or_404(Category, slug=parent_slug)
        products = products.filter(category=category)
    return render(request,
                  'shop/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})
# def show_categories(request):
#     return render(request, 'shop/product/categories.html', {'Categories': Category.objects.all()})

from cart.forms import CartAddProductForm


def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                                id=id,
                                slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm(product_id=id)
    return render(request, 'shop/product/detail.html', {'product': product,
                                                        'cart_product_form': cart_product_form})

