from django.db import models

NULLABLE = {'blank': True, 'null': True}


# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название продукта')
    model = models.CharField(max_length=100, verbose_name='Модель')  # TODO: Сделать работу с версиями
    date = models.DateField(verbose_name='Дата выхода')

    def __str__(self):
        return f'{self.name} {self.model}'

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        ordering = ['-date']


class Company(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название компании')
    contacts = models.TextField(verbose_name='Контакты')  # TODO: Сделать более развернуто
    country = models.CharField(max_length=100, verbose_name='Страна')
    city = models.CharField(max_length=100, verbose_name='Город')
    street = models.CharField(max_length=100, verbose_name='Улица')
    house = models.CharField(max_length=100, verbose_name='Номер дома')
    distributor = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Поставщик',
                                    related_name='distributors')
    balance = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Задолженность перед поставщиком')
    date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    products = models.ManyToManyField(Product, verbose_name='Продукты', **NULLABLE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'


class Order(models.Model):
    status_choices = [('cr', 'created'), ('pa', 'paid'), ('dr', 'delivered'), ('ac', 'accepted'), ('re', 'returned'), ('cl', 'closed'), ('di', 'disputed')]
    """статусы заказа 
    created - клиентом сделан заказ ( создается долг клиента)
    paid - поставщик подтвердил оплату ( в этот момент создается долг поставщика)
    delivered - поставщик доставил заказ ( в этот момент клиент может либо возвратить заказ, либо принять, в первом случае поставщик снова получает возможность отправить заказ, во втором заказ закрывается, долги списываются)
    disputed - клиент оспаривает заказ, дальнейшая судьба решается администрацией сервиса
    returned - заказ возвращен поставщику после согласования с площадкой, теперь появляется долг у поставщика перед клиентом
    closed - заказ закрывается, долги списываются
    """
    # TODO: Сделать зависимость от статуса заказа

    products = models.ManyToManyField(Product, verbose_name='Продукты', related_name='orders')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Компания-клиент', related_name='orders')
    company_distributor = models.ForeignKey(Company, on_delete=models.CASCADE, verbose_name='Поставщик',
                                            related_name='distributors')
    date = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    status = models.CharField(max_length=100, choices=status_choices, verbose_name='Статус заказа')
