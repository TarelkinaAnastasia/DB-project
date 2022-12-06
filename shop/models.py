from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey

class Category(MPTTModel):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', db_index=True, verbose_name='Родительская категория')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        unique_together = [['parent', 'slug']]
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',
                        args=[self.slug])

    # def get_absolute_parent_url(self):
    #     return reverse('shop:product_list_by_parent_category',
    #                     args=[self.slug])
# class Country(models.Model):
#     name = models.CharField(max_length=200, db_index=True)
#     slug = models.SlugField(max_length=200, db_index=True, unique=True)
#
#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'Страна'
#         verbose_name_plural = 'Страны'
#
#     def __str__(self):
#         return self.name
#
#     def get_absolute_url(self):
#         return reverse('shop:product_list_by_category',
#                         args=[self.slug])


class Product(models.Model):
    category = TreeForeignKey('Category', related_name='товары', on_delete=models.CASCADE, verbose_name='Категория')
    name = models.CharField("Название", max_length=200, db_index=True)
    slug = models.SlugField("Слаг", max_length=200, db_index=True)
    image = models.ImageField(upload_to='товары/%Y/%m/%d', blank=True)

    description = models.TextField(blank=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Количество")
    available = models.BooleanField("Наличие", default=True)
    created = models.DateTimeField("Дата создания", auto_now_add=True)
    updated = models.DateTimeField("Дата обновления", auto_now=True)



    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail',
                        args=[self.id, self.slug])

# Create your models here.
