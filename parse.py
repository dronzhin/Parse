import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint

main_url = 'https://pythondigest.ru/'

response = requests.get(main_url)

if response.status_code == 200:
    print('Зашли на страницу')

soup = BeautifulSoup(response.text, 'lxml')

class_news = 'issue issue-end issue-end'
news_div = soup.find('div', class_=class_news)
data = []
new_div_p = news_div.find_all('p')
for p in new_div_p:
    url_a = p.a['href']
    name = list(p.a)[0]
    response_a = requests.get(url_a)
    soup_a = BeautifulSoup(response_a.text, 'lxml')
    lang = soup_a.html['lang']
    classes = set()
    count = 0
    for tag in soup_a.find_all(True):
        if 'class' in tag.attrs:

            classes.update(tag['class'])
            count += 1
    data.append([name, url_a, lang, count, classes])
    print(f'Информация об новости "{name}" добавлена')

columns = ['Название новости', 'Ссылка на новость', 'Язык новости', 'Количество классов на сайте', 'Названия классов на сайте']
df = pd.DataFrame(data, columns=columns)

# Сохранение в CSV
df.to_csv('data.csv', index=True, encoding='utf-8')