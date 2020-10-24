from datetime import datetime, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand

from rate import choices
from rate.models import Rate

import requests


def to_decimal(num):
    TWOPLACES = Decimal(10) ** -2
    return Decimal(num).quantize(TWOPLACES)


class Command(BaseCommand):

    def handle(self, *args, **options):
        date_format = '%d.%m.%Y'
        start = datetime(2014, 12, 1)
        end = datetime.now()
        date_generated = [
            start + timedelta(days=x)
            for x in range(0, (end - start).days)
        ]

        for created in date_generated:
            created_str = created.strftime(date_format)
            url = 'https://api.privatbank.ua/p24api/exchange_rates'
            params = {'json': '', 'date': created_str}
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()['exchangeRate']

            source = choices.SOURCE_PRIVATBANK
            currency_map = {
                'USD': choices.CURRENCY_USD,
                'EUR': choices.CURRENCY_EUR,
            }

            for row in data:
                if row['currency'] in currency_map:
                    buy = to_decimal(row['purchaseRate'])
                    sale = to_decimal(row['saleRate'])
                    currency = currency_map[row['currency']]

                    last_rate = Rate.objects.filter(
                        source=source,
                        currency=currency,
                        created=created,
                    ).last()
                    # save accounts if record was not found or sale or buy was changed
                    if last_rate is None:
                        rate = Rate.objects.create(
                            currency=currency,
                            source=source,
                            sale=sale,
                            buy=buy,
                        )

                        rate.created = created
                        rate.save(update_fields=('created', ))
