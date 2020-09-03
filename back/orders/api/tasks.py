# from celery import task
# from django.core.mail import send_mail
# from orders.models import Order
# from time import sleep
# @task
# def order_created(order_id):
#     """
#     Task to send an e-mail notification when an order is successfully created.
#     """
#     order = Order.objects.get(id=order_id)
#     subject = f'Order nr. {order.id}'
#     message = f'You have successfully placed an order. Your order id is {order.id}.'
#     mail_sent = send_mail(subject, message, 'gowniudaykiran@gmail.com', [order.user.email])
#     return mail_sent
