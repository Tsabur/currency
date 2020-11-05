from decimal import Decimal
from itertools import zip_longest

from bs4 import BeautifulSoup

from celery import shared_task

from rate.views import parse_site_ukrsibbank

import requests

TWOPLACES = Decimal(10) ** -2


def create_object(currency, source, buy, sale):
    from rate.models import Rate
    last_rate = Rate.objects.filter(currency=currency, source=source).last()
    if last_rate is None or buy != last_rate.buy or sale != last_rate.sale:
        Rate.objects.create(
            currency=currency,
            source=source,
            buy=buy,
            sale=sale,
        )


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

    for row in data:
        if (row['currencyCodeA'] or row['currencyCodeB']) not in currency_map:
            break
        elif row['currencyCodeA'] and row['currencyCodeB'] in currency_map:
            buy = Decimal(row['rateBuy']).quantize(TWOPLACES)
            sale = Decimal(row['rateSell']).quantize(TWOPLACES)
            currency = currency_map[row['currencyCodeA']]

            create_object(currency, source, buy, sale)


@shared_task
def parse_vkurse():
    url = 'http://vkurse.dp.ua/course.json'
    response = requests.get(url)

    response.raise_for_status()
    data = response.json()

    source = 3
    currency_map = {
        'Dollar': 1,
        'Euro': 2,
    }

    for row in data:
        if row in currency_map:
            buy = Decimal(data[row]['buy']).quantize(TWOPLACES)
            sale = Decimal(data[row]['sale']).quantize(TWOPLACES)
            currency = currency_map[row]

            create_object(currency, source, buy, sale)


@shared_task
def parse_ukrsibbank():
    data = parse_site_ukrsibbank()

    source = 4
    currency_map = {
        'usd': 1,
        'eur': 2,
    }

    for row in data:
        if row['ccy'] in currency_map:
            buy = Decimal(row['buy']).quantize(TWOPLACES)
            sale = Decimal(row['sale']).quantize(TWOPLACES)
            currency = currency_map[row['ccy']]

            create_object(currency, source, buy, sale)


@shared_task
def parse_aval():
    url = 'https://ex.aval.ua/ru/personal/everyday/exchange/exchange/'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    rows = soup.find_all('td', attrs={'class': "name"})
    list1 = [i.text for i in rows]
    rows = soup.find_all('td', attrs={'class': "right"})
    list2 = [i.text for i in rows]
    list_usd = []
    list_usd.append(list1[7])
    list_usd.append(list2[-4])
    list_usd.append(list2[-3])
    list_eur = []
    list_eur.append(list1[8])
    list_eur.append(list2[-2])
    list_eur.append(list2[-1])

    list_data = ['ccy', 'buy', 'sale']

    usd = dict(zip_longest(list_data, list_usd))
    eur = dict(zip_longest(list_data, list_eur))

    data = []
    data.append(usd)
    data.append(eur)

    source = 5
    currency_map = {
        '$': 1,
        '€': 2,
    }

    for row in data:
        if row['ccy'] in currency_map:
            buy = Decimal(row['buy']).quantize(TWOPLACES)
            sale = Decimal(row['sale']).quantize(TWOPLACES)
            currency = currency_map[row['ccy']]

            create_object(currency, source, buy, sale)


@shared_task
def parse_oschadbank():
    url = 'https://www.oschadbank.ua/ua/private/currency'
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('td', attrs={'class': 'text-right'})
    result = [i.text for i in rows]

    source = 6
    currency_map = {
        '840': 1,
        '978': 2,
    }

    for key, currency in currency_map.items():
        currency_index = result.index(key)
        buy, sale = (Decimal(result[currency_index + 4 + i]).quantize(TWOPLACES) for i in range(2))

        create_object(currency, source, buy, sale)
