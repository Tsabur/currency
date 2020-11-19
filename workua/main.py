import json
import os
import random
import sqlite3
from time import sleep

from bs4 import BeautifulSoup

from fake_useragent import UserAgent

import requests


def random_sleep():
    sleep(random.randint(1, 5))


# def remove_result():
#     try:
#         os.remove('./results.txt')
#     except FileNotFoundError:
#         pass


def write_to_file(**kwargs):
    with open('./results.txt', 'a') as file:
        row = ', '.join(
            f'{key}: {value}' for key, value in kwargs.items()
        )
        file.write(row + '\n')


def write(_format='file', **kwargs):
    if _format == 'file':
        write_to_file(**kwargs)
    if _format == 'sqlite':
        write_to_db(**kwargs)
    # if _format == 'json':
    #     write_to_json(**kwargs)


def clean_trash(string):
    if string is None:
        return None
    trashs = ['\u202f', '\u2009', '\n', '\xa0', '  ', ';', "'", '-']

    for trash in trashs:
        if trash in string:
            string = string.replace(trash, '')
    return string


def main():
    # remove_result()

    counter = 0
    ua = UserAgent()

    while True:
        random_sleep()
        counter += 1
        # print(f'Page:{counter}')

        if counter == 6:
            break

        headers = {
            'User-Agent': ua.random,
                   }
        query_params = {
            'page': counter,
        }
        url = 'https://www.work.ua/jobs/'
        response = requests.get(url, params=query_params, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        job_list = soup.find('div', {'id': 'pjax-job-list'})

        # if not job_list:
        if job_list is None:
            break

        job_set = job_list.find_all('h2')

        if not job_set:
            break

        for job in job_set:
            a_tag = job.find('a', href=True)
            href_job = a_tag['href']
            title = a_tag['title']
            # content = a_tag.text
            # write(href=href_job, title=title, content=content)
            # print(f'href: {href_job}, title: {title}, content: {content}')

            url_job = 'https://www.work.ua' + href_job

            response = requests.get(url_job)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')
            job_info = soup.find('div', {'class': "card wordwrap"})

            salary = job_info.find('b', {'class': "text-black"})

            if salary is None:
                salary = None
            else:
                salary = salary.text

            company_tag = job_info.find('a', href=True, title=True)
            company_href = company_tag['href']
            company_name = company_tag.text

            company_type = job_info.find('span', {'class': 'add-top-xs'}).next
            company_size = company_type.next.next

            company_adress = job_info.find(
                'span', {'class': 'glyphicon glyphicon-map-marker text-black glyphicon-large',
                         'title': 'Адреса роботи'}
            ).next

            company_conditions = job_info.find(
                'span', {'class': 'glyphicon glyphicon-tick text-black glyphicon-large',
                         'title': 'Умови й вимоги'}
            ).next

            value = [clean_trash(i) for i in (
                salary, company_href, company_name, company_type, company_size, company_adress, company_conditions
            )]
            value.insert(0, href_job)

            trash = ['\u202f', '\u2009', '\n', '\xa0', '  ', "'", '-']
            for i in trash:
                if i in title:
                    title = title.replace(i, '')
            value.insert(1, title)

            keys = (
                'href_job', 'title', 'salary', 'company_href', 'company_name',
                'company_type', 'company_size', 'company_adress', 'company_conditions'
            )

            data = dict(zip(keys, value))

            with open('./results.json', 'a') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
            write(**data)


def write_to_db(**kwargs):
    name_db = 'mydatabase.db'
    cur_dir = os.getcwd()
    path_db = os.path.join(cur_dir, name_db)

    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cursor.execute('''Create table IF NOT EXISTS 'Jobs info'
    (href_job text, title text, salary text, company_href text,
    company_name text, company_type text, company_size text, company_adress text, company_conditions text)
    ''')

    conn.commit()

    values = ["'empty'" if i is None else f"'{i}'" for i in kwargs.values()]
    # for i in kwargs.values():
    #     if i is None:
    #         values = ["'empty'"]
    #     else:
    #         values = [f"'{i}'"]

    # print(f"INSERT INTO 'Jobs info' VALUES ({', '.join(values)})")

    cursor.execute(f"INSERT INTO 'Jobs info' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
    # cursor.execute(f"INSERT INTO 'Jobs info' VALUES ({', '.join(values)})")

    conn.commit()
    conn.close()


# def write_to_json(**kwargs):
#     with open('./results.json', 'w') as json_file:
#         json.dump(main(), json_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    main()
