# from django.core.cache import cache
from django.db import models

from rate import choices


class Rate(models.Model):
    currency = models.PositiveSmallIntegerField(choices=choices.CURRENCY_CHOISES, db_index=True)
    source = models.PositiveSmallIntegerField(choices=choices.SOURCE_CHOICES)
    buy = models.DecimalField(max_digits=6, decimal_places=2)
    sale = models.DecimalField(max_digits=6, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        index_together = (
            ('currency', 'source'),
        )

        permissions = [
            ("full_edit", "This permissions allows user to update all available fields in Rate model")
        ]

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     key = self.__class__.cache_key(self.currency, self.source)
    #     cache.delete(key)
    #
    # @classmethod
    # def cache_key(cls, currency, source):
    #     import hashlib
    #     return hashlib.md5(f"Rate:{currency}_{source}".encode()).hexdigest()


class ContactUs(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=128)
    text = models.TextField()


class Feedback(models.Model):
    rating = models.PositiveSmallIntegerField(choices=choices.RATING_CHOICE)
