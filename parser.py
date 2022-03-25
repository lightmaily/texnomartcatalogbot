import sqlite3
import requests
import re
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

load_dotenv()
HOST = os.getenv('HOST')
URL = os.getenv('URL')

db = sqlite3.connect('texnomart.db')
cursor = db.cursor()


def start_parser():
    response = requests.get(URL)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    categories = soup.find_all('div', class_='category__item')

    for info in categories:
        info_title = info.find('h2', class_='content__title').get_text(strip=True)
        info_name = info.find_all('li', class_='content__item')
        print(info_title)

        for li in info_name:
            li_title = li.find('a', class_='content__link').get_text(strip=True)
            li_intro = HOST + li.find('a', class_='content__link')['href']
            li_catalogs_edited = re.findall(r'[a-zA-Zа-яА-Яё]+', li_title)
            edited_names = ' '.join(li_catalogs_edited)
            res2 = requests.get(li_intro)
            html2 = res2.text
            soup2 = BeautifulSoup(html2, 'html.parser')
            container = soup2.find_all('div', class_='category__content')
            for article in container:
                article_title = article.find('h2', class_='content__title').get_text(strip=True)
                article_intro = HOST + article.find('a')['href']
                print(article_title)
                print(article_intro)
                cursor.execute('''
                    INSERT OR IGNORE INTO categories(category_name) VALUES (?)
                ''', (info_title,))
                cursor.execute('''
                    SELECT category_name FROM categories WHERE category_name = ?
                ''', (info_title,))
                idi = cursor.fetchone()[0]
                cursor.execute('''
                    INSERT OR IGNORE INTO under_catalogs(category_name, under_catalog_name) VALUES (?,?)
                ''', (idi, edited_names))
                cursor.execute('''
                    INSERT OR IGNORE INTO under_categories(under_catalog_name, under_category_name, under_category_link) 
                    VALUES (?,?,?)
                ''', (edited_names, article_title, article_intro))
                db.commit()




start_parser()
