from decimal import Decimal

from celery import shared_task

# from rate.views import parse_site_ukrsibbank

import requests


@shared_task
def parse_privatbank():
    from rate.models import Rate
    url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'
    response = requests.get(url)
    # raise error if response.status_code != 200
    response.raise_for_status()
    data = response.json()

    source = 1
    currency_map = {
        'USD': 1,
        'EUR': 2,
    }

    TWOPLACES = Decimal(10) ** -2
    for row in data:
        if row['ccy'] in currency_map:
            buy = Decimal(row['buy']).quantize(TWOPLACES)
            sale = Decimal(row['sale']).quantize(TWOPLACES)
            currency = currency_map[row['ccy']]

            last_rate = Rate.objects.filter(currency=currency, source=source).last()
            # save rate if record was not found or buy or sale was changed
            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    buy=buy,
                    sale=sale,
                )


@shared_task
def parse_monobank():
    from rate.models import Rate
    url = 'https://api.monobank.ua/bank/currency'
    response = requests.get(url)

    response.raise_for_status()
    data = response.json()

    source = 2
    currency_map = {
        840: 1,
        978: 2,
        980: 3,
    }

    TWOPLACES = Decimal(10) ** -2
    for row in data:
        if (row['currencyCodeA'] or row['currencyCodeB']) not in currency_map:
            break
        elif row['currencyCodeA'] and row['currencyCodeB'] in currency_map:
            buy = Decimal(row['rateBuy']).quantize(TWOPLACES)
            sale = Decimal(row['rateSell']).quantize(TWOPLACES)
            currency = currency_map[row['currencyCodeA']]

            last_rate = Rate.objects.filter(currency=currency, source=source).last()

            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    buy=buy,
                    sale=sale,
                )


@shared_task
def parse_vkurse():
    from rate.models import Rate
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)

    response.raise_for_status()
    data = response.json()

    source = 3
    currency_map = {
        'Dollar': 1,
        'Euro': 2,
    }

    TWOPLACES = Decimal(10) ** -2
    for row in data:
        if row in currency_map:
            buy = Decimal(data[row]['buy']).quantize(TWOPLACES)
            sale = Decimal(data[row]['sale']).quantize(TWOPLACES)
            currency = currency_map[row]

            last_rate = Rate.objects.filter(currency=currency, source=source).last()

            if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
                Rate.objects.create(
                    currency=currency,
                    source=source,
                    buy=buy,
                    sale=sale,
                )


# @shared_task
# def parse_ukrsibbank():
#     from rate.models import Rate
#
#     data = parse_site_ukrsibbank()
#
#     source = 3
#     currency_map = {
#         'usd': 1,
#         'eur': 2,
#     }
#
#     TWOPLACES = Decimal(10) ** -2
