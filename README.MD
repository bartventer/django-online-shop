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
## Home Page / Product Catalog
1

## Product detail view
2

## Cart view
3

## Create a coupon on the admin site
Create
4
Success
5

## Apply coupon to cart
Apply
6
Success
7

## Checkout cart
Checkout
8
Fill out details and process order
9

# Order processed via Celery and RabbitMQ
RabbitMQ is configured as the broker and Celery workers execute the queued tasks.
Client receives email
10
Monitor Celery async task execution on Flower.
11


## Process payment
RabbitMQ is configured as the broker and Celery workers execute the queued tasks.

Fill out details
[Braintree sanbox test account details below]
12

Payment processed
13

Client receives an email notication with an invoice attached
14
15

Monitor Celery async task execution on Flower
15.1

## Admin site
Login
16

Home
17

Orders view
Shows order status (paid/unpaid), and includes a few custom functions such as to view the detail order, download to csv, or print the pdf invoice (same as invoice screenshot above as received by the client)
18
19
