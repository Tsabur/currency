# from django.shortcuts import render
from itertools import zip_longest

from bs4 import BeautifulSoup

from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from rate.models import ContactUs, Feedback, Rate

from selenium import webdriver

# import requests
# import html5lib
# import lxml
# import json
# from urllib.request import urlopen
# import codecs


def parse_site_ukrsibbank():
    # путь к драйверу chrome
    chromedriver = '/opt/local/bin/chromedriver'
    options = webdriver.ChromeOptions()
    options.add_argument('headless')  # для открытия headless-браузера
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

    browser.get('https://my.ukrsibbank.com/ru/personal/operations/currency_exchange/')
    # Получение HTML-содержимого
    requiredHtml = browser.page_source

    soup = BeautifulSoup(requiredHtml, 'html5lib')
    table = soup.findChildren('table')
    my_table = table[0]
    # получение тегов и печать значений
    rows = my_table.findChildren(['th', 'tr'])

    result = ''
    for row in rows:
        cells = row.findChildren('td')
        for cell in cells:
            value = cell.text
            result += value + '/'

    result = result.lower()
    rus_dict = 'йцукенгшщзхъфывапролджэёячсмитьбю'
    result_new = ''
    for i in result:
        if i in rus_dict:
            i.replace(i, '')
        else:
            result_new += i

    result_new = result_new.replace('/', '', 4).replace(' ', '').replace(',', '').split('/')
    del result_new[8:]
    list_usd = result_new[:3]
    list_eur = result_new[4:7]

    list_data = ['ccy', 'buy', 'sale']

    usd = dict(zip_longest(list_data, list_usd))
    eur = dict(zip_longest(list_data, list_eur))

    data = []
    data.append(usd)
    data.append(eur)
    return data


class RateListView(ListView):
    queryset = Rate.objects.all()


class CreateContactUsView(CreateView):
    success_url = reverse_lazy('index')
    model = ContactUs
    fields = ('email', 'subject', 'text')

    # def form_valid(self, form):
    #     #TODO send message
    #     return super().form_valid(form)


class CreateFeedbackView(CreateView):
    model = Feedback
    fields = ('rating')
