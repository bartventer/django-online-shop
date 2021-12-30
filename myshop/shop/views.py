from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender

def product_list(request, category_slug=None):
    '''Product catelog view, or catelog view filtered by a category.
    
    Args:
        category_slug: Optional, the category slug field from the Category model.

    Returns:
        Product catelog template for all categories or for the filtered category.
    '''
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available = True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(
        request,
        'shop/product/list.html',
        {
            'category':category,
            'categories':categories,
            'products':products
        }
    )

def product_detail(request, id, slug):
    '''Detail view of a single product.

    Args:
        id: The id field of the Product model.
        slug: The slug field of the Product model.

    Returns:
        Detail product template for a selected product.
    '''
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    r = Recommender()
    recommended_products = r.suggest_products_for([product],4)

    return render(
        request,
        'shop/product/detail.html',
        {'product':product,
        'cart_product_form':cart_product_form,
        'recommended_products':recommended_products}
    )
    