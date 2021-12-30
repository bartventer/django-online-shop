from decimal import Decimal
from django.conf import settings
from shop.models import Product
from coupons.models import Coupon

class Cart(object):
    '''Cart class to manage the shopping cart.'''
    def __init__(self, request):
        '''Initialize the cart.
        
        Args:
            request: A http request object.

        Returns:
            None
        '''
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            #save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

        #a cart is a dictionary with product ID's as keys, for each product ID, the value is
        # a dictionary which includes quantity and price key-value pairs
        self.cart = cart
        # store current applied coupon
        self.coupon_id = self.session.get('coupon_id')


    def add(self, product, quantity=1, override_quantity=False):
        '''Add a product to the cart or update its quantity.
        
        Args:
            product (Product object): The product instance to add or update in the cart.
            quantity (int): Optional, an integer with the product quantity. Defaults to 1.
            override_quantity (bool): Boolean which indicates whether the quantity needs to
                be overridden with the given quantity (True), or whether new quantity has to
                be added to the existing quantity (False).

        Returns:
            None
        '''
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}

        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()
        

    def save(self):
        '''Mark the session as 'modified' to make sure it gets saved.
        
        Args:
            None
        
        Returns:
            None
        '''
        self.session.modified = True


    def remove(self, product):
        '''Remove a product from the cart.
        
        Args:
            product (Product object): The product instance to be removed from the cart.

        Returns:
            None
        '''
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
        

    def __iter__(self):
        '''Iterate over the items in the cart and get the products from the database.'''
        product_ids = self.cart.keys()
        # get the product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            # add the product instance to the cart
            cart[str(product.id)]['product'] = product
        
        for item in cart.values():
            # note the product price is the same as the first time the user added it to the cart
            # the price is not subsequently updated, regardless of updates in the database.
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item
        

    def __len__(self):
        '''Count all items in the cart and return an integer.'''
        return sum(item['quantity'] for item in self.cart.values())


    def get_total_price(self):
        '''Return the total cost of the cart.'''
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())


    def clear(self):
        '''Remove the cart from the session.'''
        del self.session[settings.CART_SESSION_ID]
        self.save()


    @property
    def coupon(self):
        '''The method is defined as an attribute by use of the property
        decorator. If the coupon_id is an attribute of the cart, then
        the Coupon object with the corresponding ID is returned.
        '''
        if self.coupon_id:
            try:
                return Coupon.objects.get(id=self.coupon_id)
            except Coupon.DoesNotExist:
                pass
        return None
    

    def get_discount(self):
        '''Method that retrieves the discount rate, if the cart contains a coupon,
        and returns the amount to be deducted from the total amount of the cart.'''
        if self.coupon:
            return (self.coupon.discount / Decimal(100)) * self.get_total_price()
        return Decimal(0)
    

    def get_total_price_after_discount(self):
        '''Method that returns the remaineder after deducting the discount (get_discount method)
        from the total amount of the cart (get_total_price method).'''
        return self.get_total_price() - self.get_discount()

    @property
    def is_empty(self):
        '''Returns True if the len of the cart is 0, else returns False.'''
        return self.cart.__len__()==0
