from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import override
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from coupons.forms import CouponApplyForm
from shop.recommender import Recommender


@require_POST
def cart_add(request, product_id):
    '''View for adding products to the cart, or updating existing quantities.
    
    Args:
        request: The HTTP request object.
        product_id: The ID for the object from the Product model.

    Returns:
        Redirects to the cart detail URL, which will display all the contents
        of the cart.
    '''
    cart = Cart(request)
    product = get_object_or_404(Product, id = product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd['quantity'],
            override_quantity=cd['override']
        )
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    '''View to remove items from the cart.
    
    Args:
        request: The HTTP request object.
        product_id: The ID for the object from the Product model.

    Returns:
        Redirects to the cart detail URL, which will display all the contents
        of the cart.
    '''
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    '''View which renders the cart and its items.'''
    cart = Cart(request)
    for item in cart:
        #create  an instance of the CartAddProductForm for each item to allow changing quantities
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity':item['quantity'], 'override':True})
    coupon_apply_form = CouponApplyForm()

    if not cart.is_empty:
        r = Recommender()
        cart_products = [item['product'] for item in cart]
        recommended_products = r.suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = None

    return render(
        request,
        'cart/detail.html',
        {'cart':cart,
        'coupon_apply_form':coupon_apply_form,
        'recommended_products':recommended_products}
        )




