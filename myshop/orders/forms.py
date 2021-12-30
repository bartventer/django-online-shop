from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    '''Form used to post information about the user.
    
    This is a ModelForm, the save() method should be performed on the 
    instantiated object to save the posted data to the Order Model.'''
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'postal_code', 'city']