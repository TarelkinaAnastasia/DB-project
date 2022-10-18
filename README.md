# DB-project

# Описание
Интернет-магазин осуществляющий следующий функционал:

1) создание базы данных продуктов и их категорий

2) добавление продуктов в корзину и сохранение в пределах сессий Django

3) создание функционала оформления заказа и добавления заказа в БД
## Наименование
Интернет-магазин чая
## Предметная область
Интернет-торговля
# Данные
Категории товаров, Товары, Заказы
## Для каждого элемента данных - ограничения
Category[name(varchar 200), slug(varchar 200)]

Product[category(ForeignKey Category), name(varchar 200), slug(varchar 200), image(varchar 200), decription(text), price(decimal(10,2)), stock(integer), available(boolean), created(timestamp [ (0) ] [ without time zone ]), updated(timestamp [ (0) ] [ without time zone ])]

Order [order id(integer), slug_product(ForeignKey Product), amount (integer), order_cost(decimal(10,2)) , created(timestamp [ (0) ] [ without time zone ]), updated(timestamp [ (0) ] [ without time zone ]), address(varchar 200), email(varchar 200), status(varchar 200)]
## Общие ограничения целостности
При удалении категории - удаляются товары этой категории, но при наличии заказа с товаром - товар невозможно удалить.
# Пользовательские роли
## Для каждой роли - наименование, ответственность, количество пользователей в этой роли?
Работник магазина : добавление категорий, товаров, просмотр заказов, изменение статуса. Количество пользователей - 1.
Покупатель: добавление товара в корзину, оформление заказа. Количество пользователей - 1000.
# UI / API 
ui - сайт
# Технологии разработки
## Язык программирования
Python(Django)
## СУБД
PostgreSQL
# Тестирование
Ручное тестирование
