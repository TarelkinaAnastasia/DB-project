from celery import shared_task
from django.core.mail import send_mail
from .models import Order, OrderItem
from shop.models import Product
from django.conf import settings


@shared_task
def order_created(order_id):
    """
    Задача для отправки уведомления по электронной почте при успешном создании заказа.
    """
    order = Order.objects.get(id=order_id)
    order_items = list(OrderItem.objects.filter(order=order_id))
    subject = 'Заказ номер  {}'.format(order_id)
    message = 'Здравствуйте {},\n\nВаш заказ успешно создан.\
                Ваш идентификационный номер {}.'.format(order.first_name, order.id)
    order_items_str = '\n'.join(['{0: <50} {1: >13} {2: >15}₽'.format(item.product.name, \
                                                    'x' + str(item.quantity), str(item.price)) for item in order_items])
    message = f"Здравствуйте {order.first_name},\n\nВаш заказ №{order.id} успешно создан.\n\
Адрес доставки: {order.city}, {order.postal_code}, {order.address}\n\
Вы заказали:\n\
{order_items_str}\n\
{'{0: <63} {1: >16}₽'.format('Итого:', str(order.get_total_cost()))}\n\
Спасибо за заказ  !"
    mail_sent = send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[order.email],
                    fail_silently=False,)
    return mail_sent

#{'{0: <50} {1: >13} {2: >15}'.format('Товар', 'Количество', 'Стоимость')}\n\