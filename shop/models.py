from django.db import models
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from django_resized import ResizedImageField
# from PIL import Image

from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


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
    image = ResizedImageField(size=[600, 600], crop=['middle', 'center'], upload_to='товары/%Y/%m/%d', blank=True)
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

    # def save(self, *args, **kwargs):
    #     img = Image.open(self.image)  # Open image using self
    #     if img:
    #         new_img = (300, 300)
    #         img.thumbnail(new_img)
    #         img.save(self.image)  # saving image at the same path
    #         print(img)
    #
    #     super(Product, self).save(*args, **kwargs)


# @receiver(pre_delete, sender=Product)
# def mymodel_delete(sender, instance, **kwargs):
#     # Pass false so FileField doesn't save the model.
#     instance.file.delete(False)
# Create your models here.
