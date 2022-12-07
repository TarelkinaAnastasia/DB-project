from celery import shared_task
from django.core.mail import send_mail
from .models import Order
from django.conf import settings

@shared_task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    subject = 'Заказ номер  {}'.format(order_id)
    message = 'Здравствуйте {},\n\nВаш заказ успешно создан.\
                Ваш идентификационный номер {}.'.format(order.first_name,
                                             order.id)
    mail_sent = send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[order.email],
                    fail_silently=False,)
    return mail_sent