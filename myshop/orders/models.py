import decimal
from django.core import validators
from django.db import models
from shop.models import Product
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon


class Order(models.Model):
    '''Order Model to store order detail.'''
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True,on_delete=models.CASCADE)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])


    class Meta:
        ordering = ('-created',)


    def __str__(self):
        return f'Order {self.id}'


    def get_total_cost(self):
        'Returns the total cost of all items in the order, after subtracting discounts.'
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost*(self.discount/Decimal(100))


    def get_discount(self):
        if self.coupon:
            return (self.discount / Decimal(100)) * self.get_total_cost()/((Decimal(100)-self.discount)/Decimal(100))
        return Decimal(0)


class OrderItem(models.Model):
    '''OrderItem Model to store items bought.
    
    Fields:
        order: ForeignKey field to the Order Model.
        product: ForeignKey field from the Product Model.
        price: Price decimal field.
        quantity: Quantity positive integer field.
    '''
    order = models.ForeignKey(to=Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        'Returns the total cost of the order by mutliplying the unit price and quantity.'
        return self.price *self.quantity