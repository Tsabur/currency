from unittest.mock import MagicMock

from rate.models import Rate
from rate.tasks import parse_aval, parse_monobank, parse_oschadbank, parse_privatbank, parse_ukrsibbank, parse_vkurse


def test_parse_privatbank(mocker):
    count_rates = Rate.objects.count()
    currencies = [{"ccy": "USD", "base_ccy": "UAH", "buy": "28.30000", "sale": "28.70000"},
                  {"ccy": "EUR", "base_ccy": "UAH", "buy": "32.95000", "sale": "33.56000"},
                  {"ccy": "RUR", "base_ccy": "UAH", "buy": "0.35300", "sale": "0.39300"},
                  {"ccy": "BTC", "base_ccy": "USD", "buy": "13453.7062", "sale": "14869.8858"}]
    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = MagicMock(
        status_code=200,
        json=lambda: currencies
    )
    parse_privatbank()
    assert Rate.objects.count() == count_rates + 2

    # we save rates if amoun of buy or sale field was changed
    parse_privatbank()
    assert Rate.objects.count() == count_rates + 2


def test_parse_monobank(mocker):
    count_rates = Rate.objects.count()
    currencies = [
        {"currencyCodeA": 840, "currencyCodeB": 980, "date": 1604572807, "rateBuy": 28.3, "rateSell": 28.5698},
        {"currencyCodeA": 978, "currencyCodeB": 980, "date": 1604571607, "rateBuy": 33.2, "rateSell": 33.67},
        {"currencyCodeA": 643, "currencyCodeB": 980, "date": 1604527807, "rateBuy": 0.353, "rateSell": 0.38}
    ]
    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = MagicMock(
        status_code=200,
        json=lambda: currencies
    )
    parse_monobank()
    assert Rate.objects.count() == count_rates + 2

    parse_monobank()
    assert Rate.objects.count() == count_rates + 2


def test_parse_vkurse(mocker):
    count_rates = Rate.objects.count()
    currencies = {"Dollar": {"buy": "28.30", "sale": "28.50"},
                  "Euro": {"buy": "33.35", "sale": "33.55"},
                  "Rub": {"buy": "0.353", "sale": "0.362"}}
    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = MagicMock(
        status_code=200,
        json=lambda: currencies
    )
    parse_vkurse()
    assert Rate.objects.count() == count_rates + 2

    parse_vkurse()
    assert Rate.objects.count() == count_rates + 2


def test_parse_aval(mocker):
    count_rates = Rate.objects.count()
    with open('src/tests/parse_html/avalbank.html', 'r', encoding='ISO-8859-1', errors='ignore') as file_aval:
        text_file = '\n'.join(file_aval.readline())
    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = MagicMock(
        status_code=200,
        text=text_file
    )
    parse_aval()
    assert Rate.objects.count() == count_rates + 2

    parse_aval()
    assert Rate.objects.count() == count_rates + 2


def test_parse_oschadbank(mocker):
    count_rates = Rate.objects.count()
    with open('src/tests/parse_html/oschadbank.html', 'r', encoding='ISO-8859-1', errors='ignore') as file_oschadbank:
        text_file = '\n'.join(file_oschadbank.readline())
    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = MagicMock(
        status_code=200,
        text=text_file
    )
    parse_oschadbank()
    assert Rate.objects.count() == count_rates + 2

    parse_oschadbank()
    assert Rate.objects.count() == count_rates + 2


def test_parse_ukrsibbank(mocker):
    count_rates = Rate.objects.count()
    with open('src/tests/parse_html/ukrsibbank.html', 'r', encoding='ISO-8859-1', errors='ignore') as file_ukrsibbank:
        text_file = '\n'.join(file_ukrsibbank.readline())
    requests_get_patcher = mocker.patch('requests.get')
    requests_get_patcher.return_value = MagicMock(
        status_code=200,
        text=text_file
    )
    parse_ukrsibbank()
    assert Rate.objects.count() == count_rates + 2

    parse_ukrsibbank()
    assert Rate.objects.count() == count_rates + 2
