import requests
from bs4 import BeautifulSoup
import csv
import pandas as panda
from datetime import datetime


url = 'https://www.akchabar.kg/ru/exchange-rates/'
#Агент чтобы сайт не распознал нас за бота
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML,'
                         ' like Gecko) Chrome/103.0.0.0 Safari/537.36'}



def get_data():
    global table
    # parser-lxml = Преобразовать html в удобный для Python формат
    # Получить информацию о странице
    pages = requests.get(url)
    soup = BeautifulSoup(pages.text, 'lxml')
    # Получить информацию из тега <table>
    table = soup.find('table', id='rates_table')

get_data()

headers = ['Банк:', 'Покупка USD', 'Продажа USD',
           'Покупка EURO', 'Продажа EURO',
           'Покупка RUB', 'Продажа RUB',
           'Покупка KZT', 'Продажа KZT']


def parse():
    # Создаем цикл for для заполнения данных
    # Создаем фрейм данных
    data = panda.DataFrame(columns=headers)
    for item in table.find_all('tr')[1:]:
        row_data = item.find_all('td')
        row = [i.text for i in row_data]
        length = len(data)
        data.loc[length] = row
    # Удаление и очистка ненужных строк
    data.drop(labels=[0], axis=0, inplace=True)
    #Установки даты
    date_time = datetime.now().strftime('%d_%m_%Y')
    # Экспорт в csv
    data.to_csv(f'last_data{date_time}.csv', index=False)
    # Прочитать csv
    data2 = panda.read_csv(f'last_data{date_time}.csv')


parse()





