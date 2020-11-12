import os
import random
import sqlite3
from time import sleep

from bs4 import BeautifulSoup

from fake_useragent import UserAgent

import requests


def write_to_db():
    name_db = 'mydatabase.db'
    cur_dir = os.getcwd()
    path_db = os.path.join(cur_dir, name_db)

    conn = sqlite3.connect(path_db)
    cursor = conn.cursor()

    cursor.execute("""Create table
    (href text, title text, content text, date text, company text, city text, conditions text, description text)
    """)


def random_sleep():
    sleep(random.randint(1, 5))


def remove_result():
    try:
        os.remove('./results.txt')
    except FileNotFoundError:
        pass


def write_to_file(**kwargs):
    with open('./results.txt', 'a') as file:
        row = ', '.join(
            f'{key}: {value}' for key, value in kwargs.items()
        )
        file.write(row + '\n')


def write(_format='file', **kwargs):
    if _format == 'file':
        write_to_file(**kwargs)


def main():
    remove_result()

    counter = 0
    ua = UserAgent()

    while True:
        random_sleep()
        counter += 1
        print(f'Page:{counter}')

        # if counter == 4:
        #     break

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
            href = a_tag['href']
            title = a_tag['title']
            content = a_tag.text
            write(href=href, title=title, content=content)


if __name__ == '__main__':
    main()
