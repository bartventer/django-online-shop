from django import forms

class CouponApplyForm(forms.Form):
    '''Form for user to enter a coupon code.'''
    code = forms.CharField()