import braintree
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from orders.models import Order
from .tasks import payment_completed

# instantiate Braintree payment gateway
gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)

def payment_process(request):
    '''View for processing payments.

    The following actions are taken:
    1. Retrieve the current order from the order_id session key (previously
    stored in the session by the order_create view).
    2. Retrieve the Order object for the given ID or raise an HTTP404 exception
    if it is not found.
    3. If the view is loaded with a POST request, retrieve the payment_method_nonce
    to generate a new transaction using gateway.transaction, passing the following
    paramaters:
        amount: Total amount to charge the customer, which is a string with the total
            amount formatted with two decimal places.
        payment_method_nonce: The token nonce generated by Braintree for the payment.
            It will generate in the template using the JavaScript SDK.
        options: Sends the submit_for_settlement option with True so that the transaction
            is automatically submitted for settlement.
    4. If the transaction is successfully processed, mark the order as paid by settings
    its paid attribute to True and store the unique transaction ID returned by the gateway
    in the braintree_id attribute. Finally, redirects the user to the payment:done URL
    if the payment is successful, otherwise, redirect the user to payment:canceled.
    5. If the view was loaded by a GET request, generate a client token with 
    gateway.client_token.generate() to be used in the in the template to instantiate
    the Braintree JavaScript client.
    '''
    order_id = request.session.get('order_id')
    order = get_object_or_404(Order, id=order_id)
    total_cost = order.get_total_cost()

    if request.method=='POST':
        # retrieve nonce
        nonce = request.POST.get('payment_method_nonce', None)
        # create and submit transaction
        result = gateway.transaction.sale({
            'amount':f'{total_cost:.2f}',
            'payment_method_nonce':nonce,
            'options':{
                'submit_for_settlement':True
            }
        })
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
            # launch asynchronous task
            payment_completed.delay(order.id)
            return redirect('payment:done')
        else:
            return redirect('payment:canceled')
    else:
        # generate token
        client_token = gateway.client_token.generate()
        return render(
            request,
            'payment/process.html',
            {
                'order':order,
                'client_token': client_token
            }
        )

def payment_done(request):
    '''View for successful payments.'''
    return render(request, 'payment/done.html')

def payment_canceled(request):
    '''View for canceled payments.'''
    return render(request, 'payment/canceled.html')

