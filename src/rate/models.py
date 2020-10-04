from django.db import models


class Rate(models.Model):
    CURRENCY_CHOISES = (
        (1, 'USD'),
        (2, 'EUR'),
    )

    SOURCE_CHOICES = (
        (1, 'PrivatBank'),
        (2, 'MonoBank'),
        (3, 'vkurse'),

    )

    currency = models.PositiveSmallIntegerField(choices=CURRENCY_CHOISES)
    source = models.PositiveSmallIntegerField(choices=SOURCE_CHOICES)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
