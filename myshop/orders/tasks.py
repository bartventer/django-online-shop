from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings

@shared_task
def order_created(order_id):
    '''Task to build an email notification when an order is successfully created.
    
    Args:
        order_id: id of the order object.

    Returns:
        send_email() function provided by Django to send an email notification to the user who placed the order.
    '''
    # Query the Order Model for the to obtain the Order object.
    order = Order.objects.get(id=order_id)
    subject = f'Order nr. {order.id}'
    message = f'Dear {order.first_name},\n\nYou have successfully placed an order. Your order ID is {order.id}.'
    mail_sent = send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[order.email]
    )
    return mail_sent