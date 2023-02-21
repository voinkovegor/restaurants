import os
import django
from django.contrib.gis.geos import Point

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurants.restaurants.settings")
django.setup()

from list_rest.models import Restaurant

import json
import time

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


def get_source_html(url, name):
    browser = webdriver.Chrome(executable_path='/home/egor/PycharmProjects/parsing_restaurants/restaurants/list_rest/parsing/chromedriver')

    try:
        browser.get(url=url)
        browser.maximize_window()
        time.sleep(1)

        end_page_element = browser.find_elements(By.CLASS_NAME, 'add-business-view')
        actions = ActionChains(browser)
        while not end_page_element:    # Прокрутка страницы для прогрузки всех карточек компаний
            end_page_element = browser.find_elements(By.CLASS_NAME, 'add-business-view')
            actions.scroll(10, 200, 0, 500).perform()
            time.sleep(0)
        actions.move_to_element(to_element=end_page_element[0]).perform()   # Прогрузка последних карточек компаний
        with open(f"restaurants/list_rest/parsing/{name}_source-page.html", "w") as file:
            file.write(browser.page_source)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()

def get_data(file_path, name):
    with open(file_path) as file:
        src = file.read()

    soup = BeautifulSoup(src, 'lxml')
    elements = soup.find_all('li', class_='search-snippet-view')

    result = []

    for i in elements:
        title = i.find('div', class_='search-business-snippet-view__title').text

        adress = i.find('div', class_='search-business-snippet-view__address').text

        coord = i.find('div', class_='search-snippet-view__body _type_business')
        if coord:
            coord = coord.get('data-coordinates')
            lat, lon = [float(j) for j in coord.split(',')]
            result.append(
                {
                    'title': title,
                    'adress': adress,
                    'coord': [lat, lon]
                }
            )
        else:
            print(name, 'Координаты не найдены', elements.index(i))

    with open(f'restaurants/list_rest/fixtures/{name}_newdata.json', 'w', encoding='utf-8') as file:
        json.dump(result, file, indent=4, ensure_ascii=False)


def insert_data(file_path):
    with open(file_path, encoding='utf-8') as file:
        src = json.load(file)

    for i in src:
        if i['title'] == 'Kentucky Fried Chicken':
            i['title'] = 'KFC'
        Restaurant.objects.create(
            title=i['title'],
            adress=i['adress'],
            coord=Point(i['coord'])
        )



urls = {
    'Burger King': 'https://yandex.ru/maps/213/moscow/chain/burger_king/1417549642/?ll=37.656323%2C55.736387&sctx=ZAAAAAgCEAAaKAoSCa7YX3ZP6EJAEXb9gt2w30tAEhIJMdC1L6C3BUARiZXRyOcV7D8iBgABAgMEBSgKOABA1QFIAWImcmVsZXZfZmlsdGVyX2Fkc19kcmFnX3RvX3pvb21fd2luZG93PTFqAnJ1nQHNzEw9oAEAqAEAvQG83fc%2FwgGKAYDMrv8D%2Fqesq4ABoej3tY8Fk4T2kgWxxIyIBvretc2IBPW5oIK3AdSXysUExeejjdAFhsihuvACmdGNpgXWmPiPrwOD4%2B7CBKWG88%2BQBdfczLoEzvKb3AShmsKNtwKPwuvLswPT%2FtW3EMD1vYAE5df1qNACnYnOnga4xM7AwgKd0aT4tgL574aJBOoBAPIBAPgBAIICItCx0YPRgNCz0LXRgCDQutC40L3QsyDQvNC%2B0YHQutCy0LCKAgCSAgMyMTOaAgxkZXNrdG9wLW1hcHM%3D&sll=37.656323%2C55.736387&sspn=1.357331%2C0.438960&z=10.09',
    'KFC': 'https://yandex.ru/maps/213/moscow/chain/kfc/6003440/?ll=37.690996%2C55.737537&sctx=ZAAAAAgCEAAaKAoSCX%2B%2FmC1ZsUJAEVg4SfPHyktAEhIJMdC1L6C3BUARDwnf%2Bxs07D8iBgABAgMEBSgKOABA1QFIAWImcmVsZXZfZmlsdGVyX2Fkc19kcmFnX3RvX3pvb21fd2luZG93PTFqAnJ1nQHNzEw9oAEAqAEAvQGytQYRwgGHAfDkhOO1AdHR9KEG9OmdxgSUzt6TBdju2YIF2NuX2wTAsp3t2gaYzu66BMfR054EgIqZpNcB8Le33Qbn%2BZXshQX9%2BeiaBrXV5Pf3AZqPrdQGnebIt%2FoEmafnugSYrOrpuQPN1efK1gKjgsr2%2BgHd54Ck8gbD7bLiOb7I%2F%2BwD95KqsATU%2F4vrBeoBAPIBAPgBAIICENC80L7RgdC60LLQsCBLRkOKAgCSAgMyMTOaAgxkZXNrdG9wLW1hcHM%3D&sll=37.690996%2C55.737537&sspn=1.357331%2C0.438947&z=10.09',
    'Vkusno i tochka': 'https://yandex.ru/maps/213/moscow/chain/vkusno_i_tochka/214710996368/?ll=37.690996%2C55.737537&sll=37.690996%2C55.737537&sspn=1.357331%2C0.438947&z=10.09'
}

def main():
    for name, url in urls.items():
        get_source_html(url, name)
        get_data(f'restaurants/list_rest/parsing/{name}_source-page.html', name)
        insert_data(f'restaurants/list_rest/fixtures/{name}_data.json')


if __name__ == '__main__':
    main()











