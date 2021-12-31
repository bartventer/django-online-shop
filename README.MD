
<!-- markdownlint-disable -->
# Django Online Shop

This is an online shop application developed with Django. Clients add products to their cart, apply coupons, checkout and order the cart items and pay for the items. A recommendation engine suggests products that are usually bought together.

# Features
- Shopping cart data persisted through Django sessions
- Celery configured with RabbitMQ serving as the message broker
- Celery is used to send asynchronous notifications to the customers
- Flower is used to monitor Celery
- Payment gateway has been integrated with the Braintree API
- Orders can be exported to CSV files
- PDF invoices can be generated dynamically
- System in place for applying coupons
- Product recommendation engine developed with Redis to suggests products to clients based on the current items in their cart; the recommendation algorithm keeps track/score of historical sales data and the combination of products purchased together, which is then used to suggest those products that are usually bought together.

# Installation and setup

Download/clone/fork the repository and install the `requirements.txt` file in your virtual environment.

# Flow
## Home Page / Product Catalogue
Catalogue of products, that can be filtered.
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/1.png?raw=true)

## Product detail view
The client can add items to their cart.
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/2.png?raw=true)


## Cart view
The client can modify the quantity or remove items from their cart, apply coupon codes, or proceed to checkout.
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/3.png?raw=true)


## Create a coupon on the admin site
- Create coupon
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/4.png?raw=true)
- Success response
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/5.png?raw=true)

## Apply coupon to cart
- Apply coupon code
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/6.png?raw=true)
- Success
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/7.png?raw=true)

## Checkout cart
- Checkout
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/8.png?raw=true)
- Fill out details and process order
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/9.png?raw=true)

# Order processed via Celery and RabbitMQ
RabbitMQ is configured as the broker and Celery workers execute the queued tasks.
- Client receives email
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/10.png?raw=true)
- Monitoring Celery asynchronous task execution on Flower
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/11.png?raw=true)


## Process payment
RabbitMQ is configured as the broker and Celery workers execute the queued tasks.

- Client fills out details [Braintree sanbox test account details below]
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/12.png?raw=true)

- Payment processed
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/13.png?raw=true)

- Client receives an email notification with an invoice attached
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/14.png?raw=true)
- Invoice attachment![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/15_1.png?raw=true)

- Monitor Celery asynchronous task execution on Flower
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/15_2.png?raw=true)

## Admin site
- Login
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/16.png?raw=true)

- Home
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/17.png?raw=true)

- Orders view: shows order status (paid/unpaid), and includes a few custom functions, such as viewing the detail order, download to csv, or print the pdf invoice (same as invoice screenshot above as received by the client)
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/18.png?raw=true)
![enter image description here](https://github.com/bartventer/django-online-shop/blob/master/myshop/github_images/19.png?raw=true)
