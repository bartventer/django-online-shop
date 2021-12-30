from django import forms

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1,21)]

class CartAddProductForm(forms.Form):
    '''Form for the user to add products to the cart.
    
    Fields:
        quantity: allows the user to select a quantity between one and 20. Cource
            is set to true to convert the data to an integer.
        override: Whether the quantity has to be added (i.e. not overridden)to any existing 
            quantity in the cart for this product (False), or whether the existing quantity
            should be overriden with the given quantity (True).
    '''
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    override = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)
