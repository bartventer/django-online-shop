from django.shortcuts import redirect, render, get_object_or_404
from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
import weasyprint


def order_create(request):
    '''View to create orders.

    Args:
        request: The HTTP request object. The session attribute will be used
            to populate the cart.
    
    Returns:
        Redirects the user to the payment process template if the user posted
            the form (i.e. POST request), otherwise (i.e. GET request) renders 
                the create.html template with an empty form.
    '''
    cart = Cart(request)
    if request.method=='POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'])
            # clear the cart
            cart.clear()
            # launch asynchronous task (using celery and RabbitMQ)
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            return redirect(reverse('payment:process'))
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart':cart,'form':form})


@staff_member_required
def admin_order_detail(request, order_id):
    '''Custom admin view that takes as paramaters the HTTP request object and order_id,
    then retrieves the Order Object and renders a template to display the order. 
    
    Staff_member_required decorator is applied which checks that both the is_active and
    is_staff field of the user requesting the page is True. '''
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order':order})


@staff_member_required
def admin_order_pdf(request, order_id):
    '''View to generate a PDF invoice for an order. The staff_member_required decorator
    is used to check that only staff users can access the view.
    
    Args:
        request: The HTTP request object.
        order_id: The given order id, which is then used to retrieve the Order Object.

    Returns:
        A PDF response object.
    '''
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html',
                            {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(
            settings.STATIC_ROOT + 'css/pdf.css')])
    return response


