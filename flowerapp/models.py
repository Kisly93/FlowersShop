from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now


class Color(models.TextChoices):
    YELLOW = 'YELLOW', 'Жёлтый'
    RED = 'RED', 'Красный'
    GREEN = 'GREEN', 'Зелёный'
    ORANGE = 'ORANGE', 'Оранжевый'
    BLUE = 'BLUE', 'Синий'
    PINK = 'PINK', 'Розовый'
    BROWN = 'BROWN', 'Коричневый'
    PURPLE = 'РURPLE', 'Фиолетовый'
    WHITE = 'WHITE', 'Белый'
    BLACK = 'BLACK', 'Чёрный'


class Flower (models.Model):
    name = models.CharField(
        'название',
        max_length=50,
    )

    price = models.IntegerField(
        'цена',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000),
        ])

    class Meta:
        verbose_name = 'цветок'
        verbose_name_plural = 'цветы'

    def __str__(self):
        return f'{self.name}: {self.price} р.'


class Packaging (models.Model):
    type = models.CharField(
        'тип',
        max_length=50,
    )

    color = models.CharField(
        'цвет',
        choices=Color.choices,
        default=Color.YELLOW,
        max_length=30,
    )

    price = models.IntegerField(
        'цена',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000),
        ])

    class Meta:
        verbose_name = 'упаковка'
        verbose_name_plural = 'упаковки'

    def __str__(self):
        return f'{self.type}: {self.price} р.'


class Ribbon (models.Model):
    type = models.CharField(
        'тип',
        max_length=50,
    )

    color = models.CharField(
        'цвет',
        choices=Color.choices,
        default=Color.YELLOW,
        max_length=30,
    )

    price = models.IntegerField(
        'цена',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1000),
        ])

    class Meta:
        verbose_name = 'лента'
        verbose_name_plural = 'ленты'

    def __str__(self):
        return f'{self.type}: {self.price} р.'


class Bouquet (models.Model):
    name = models.CharField(
        'название',
        max_length=100
    )

    packaging = models.ForeignKey(
        Packaging,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='bouquets',
        verbose_name='упаковка'
    )

    ribbon = models.ForeignKey(
        Ribbon,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='bouquets',
        verbose_name='лента'
    )

    class Categories(models.TextChoices):
        WEDDING = 'WEDDING', 'На свадьбу'
        BIRTHDAY_PARTY = 'BIRTHDAY_PARTY', 'На день рождения'
        WHATEVER = 'WHATEVER', 'Пофиг'

    category = models.CharField(
        'категория букета',
        choices=Categories.choices,
        default=Categories.WHATEVER,
        max_length=30
    )

    height = models.IntegerField(
        'высота, см',
        default=0,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(200),
        ]
    )

    width = models.IntegerField(
        'ширина, см',
        default=0,
        null=True,
        blank=True,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ]
    )

    image = models.ImageField(
        'изображение букета',
        null=True,
        blank=True,
    )

    description = models.TextField(
        'описание',
        null=True,
        blank=True,
        max_length=500,
    )

    price = models.IntegerField(
        'Цена',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000),
        ]
    )

    dont_update_price = models.BooleanField(
        'Не обновлять цену',
        default=False,
        db_index=True,
    )

    class Meta:
        verbose_name = 'букет'
        verbose_name_plural = 'букеты'

    def __str__(self):
        return f'{self.pk}. {self.name} {self.category}'


class BouquetItem (models.Model):
    bouquet = models.ForeignKey(
        Bouquet,
        on_delete=models.CASCADE,
        related_name='bouquet_items',
        verbose_name='букет',
    )

    flower = models.ForeignKey(
        Flower,
        on_delete=models.CASCADE,
        related_name='bouquet_items',
        verbose_name='цветок',
    )

    color = models.CharField(
        'оттенок цветка',
        choices=Color.choices,
        default=Color.YELLOW,
        max_length=30,
    )

    quantity = models.IntegerField(
        'количество',
        db_index=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(100),
        ],
    )

    class Meta:
        verbose_name = 'цветок букета'
        verbose_name_plural = 'цветы букета'

    def __str__(self):
        return f'{self.flower.name} {self.color} {self.bouquet.name}'


class Client(models.Model):
    name = models.CharField(
        'имя клиента',
        max_length=50,
        db_index=True,
    )

    phone_number = PhoneNumberField(
        'телефон клиента',
        region='RU',
        max_length=20,
        unique=True
    )

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.name} {self.phone_number}'


class Order(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        related_name='orders',
        verbose_name='клиент',
    )

    bouquet = models.ManyToManyField(
        Bouquet,
        related_name='orders',
        verbose_name='букет',
    )

    address = models.CharField(
        'адрес доставки',
        max_length=350,
    )

    class DeliveryTime(models.TextChoices):
        URGENT = 'URGENT', 'Как можно скорее'
        t10_12 = 't10_12', 'с 10:00 до 12:00'
        t12_14 = 't12_14', 'с 12:00 до 14:00'
        t14_16 = 't14_16', 'с 14:00 до 16:00'
        t16_18 = 't16_18', 'с 16:00 до 18:00'
        t18_20 = 't18_20', 'с 18:00 до 20:00'

    delivery_time = models.CharField(
        'время доставки',
        choices=DeliveryTime.choices,
        default=DeliveryTime.URGENT,
        max_length=10,
    )

    created_datetime = models.DateTimeField(
        'дата и время заказа',
        default=now,
        editable=False,
    )

    comment = models.TextField(
        'Комментарий к заказу',
        blank=True,
    )

    class Statuses(models.TextChoices):
        TBA = 'TBA', 'На уточнении'
        ASSEMBLING = 'ASSEMBLING', 'Собирается'
        DELIVERING = 'DELIVERING', 'Доставляется'
        DONE = 'DONE', 'Выполнен'

    status = models.CharField(
        'Статус заказа',
        choices=Statuses.choices,
        default=Statuses.TBA,
        max_length=15
    )

    cost = models.IntegerField(
        'Стоимость',
        default=0,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10000),
        ]
    )

    payed = models.BooleanField(
        'Оплачен?',
        default=False
    )

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'

    def __str__(self):
        return f'{self.pk} {self.client.name} {self.delivery_time}'
