from django.db import models
from shop.models import Product


class Order(models.Model):
    first_name = models.CharField("Имя", max_length=50)
    last_name = models.CharField("Фамилия", max_length=50)
    email = models.EmailField("Почта")
    address = models.CharField("Адрес", max_length=250)
    postal_code = models.CharField("Почтовый индекс", max_length=20)
    city = models.CharField("Город", max_length=100)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    updated = models.DateTimeField("Дата изменения", auto_now=True)
    paid = models.BooleanField("Оплачен", default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Заказ {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField("Количество", default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
# Create your models here.
