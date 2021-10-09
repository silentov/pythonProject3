from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = get_user_model()


class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__.__meta.model_name.startswith(with_respect_to), reverse=True)
        return products

class LatestProducts:

    objects = LatestProductsManager()


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Имя категории')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категория', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Наименование')
    slug = models.SlugField(unique=True)
    image = models.ImageField(verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', null=True)
    price = models.DecimalField(verbose_name='Цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return self.title


class Book(Product):

    genre = models.CharField(max_length=255, verbose_name='Жанр')
    author = models.CharField(max_length=255, verbose_name='Автор')
    year = models.CharField(max_length=30, verbose_name='Год издания')
    price_of_pdf = models.DecimalField(verbose_name='Цена эл. версии', max_digits=9, decimal_places=2)

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class Audiobook(Product):

    genre = models.CharField(max_length=255, verbose_name='Жанр')
    author = models.CharField(max_length=255, verbose_name='Автор')
    year = models.CharField(max_length=30, verbose_name='Год издания')
    duration = models.CharField(max_length=30, verbose_name='Длительность')
    dictor = models.CharField(max_length=35, verbose_name='Диктор')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class Podcast(Product):

    studio = models.CharField(max_length=255, verbose_name='Студия')
    duration = models.CharField(max_length=30, verbose_name='Длительность')
    kolvo_ep = models.CharField(max_length=255, verbose_name='Количество выпусков')

    def __str__(self):
        return "{} : {}".format(self.category.name, self.title)


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    kolvo= models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.prod.title)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(verbose_name='Общая цена', max_digits=9, decimal_places=2)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    phone = models.CharField(max_length=28, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')

    def __str__(self):
        return "Покупатель: {} {}".format(self.user.first_name, self.user.last_name)


