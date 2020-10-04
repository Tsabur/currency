# from django.shortcuts import render
from bs4 import BeautifulSoup

# import requests

from selenium import webdriver

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
    return result_new
