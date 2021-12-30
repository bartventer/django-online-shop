from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm

@require_POST
def coupon_apply(request):
    '''View to validate the coupon and stores it in the user's session.
    
    The following tasks are performed:
    1. The CouponApplyForm is instantiated with the posted data, and is checked
        that the form is valid.
    2. If the form data is valid, retrieve the code from the forms cleaned_data
        dictionary. iexact field lookup is used to perform a case-insensitve exact
            match. Also check that the form is currently active and valid for the current
                datetime.
    3. Coupon ID is stored in the user's session.
    4. User is redirected to the cart_detail URL, which will display the applied coupon
        in the cart.

    Args:
        request: HTTP request object.

    Returns:
        Redirects to the cart_detail view, with the coupon_id 
            (either a valid coupon ID, or if not valid, None) included 
                in the request.session accessible context.
    '''
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id']=None
    return redirect('cart:cart_detail')


def coupon_remove(request):
    "View to remove any currently applied coupons."
    if request.session['coupon_id']:
        request.session['coupon_id']=None
    return redirect('cart:cart_detail')

