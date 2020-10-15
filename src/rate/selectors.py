from django.core.cache import cache

from rate import choices
from rate.models import Rate


def get_latest_rates():
    key = (get_latest_rates.__name__)

    if key in cache:
        rates = cache.get(key)
    else:
        rates = []
        for source_int, _ in choices.SOURCE_CHOICES:
            for currency_int, _ in choices.CURRENCY_CHOISES:
                rate = Rate.objects.filter(source=source_int, currency=currency_int).order_by('created').last()

                if rate is not None:
                    rates.append(rate)
        cache.set(key, rates, 20)
    return rates
