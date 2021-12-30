from .cart import Cart

def cart(request):
    '''Instantiate the cart using the request object and make it available to all templates.'''
    return {'cart':Cart(request)}