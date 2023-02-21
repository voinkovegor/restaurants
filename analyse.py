import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurants.settings")
django.setup()

import pandas as pd

from django.db.models import Q
from list_rest.models import Restaurant


list_near_cities = {
    "Химки", "Люберцы", "Красногорск", "Мытищи", "Балашиха",
    "Одинцово", "Королёв", "Щелково", "Жуковский", "Подольск",
    "Зеленоград", "Электросталь", "Ногинск", "Сергиев Посад",
    "Орехово-Зуево", "Серпухов", "Обнинск", "Коломна", "Калуга",
    "Тверь"
}

# Ограничение по названию и вхождению только в г. Москва, т.к. в модель попали лишние
burger = Restaurant.objects.filter(Q(title='Бургер Кинг') & ~Q(adress__contains='область'))
kfc = Restaurant.objects.filter(Q(title='KFC') & ~Q(adress__contains='область'))
vkusno = Restaurant.objects.filter(Q(title='Вкусно — и точка') & ~Q(adress__contains='область'))

for i in list_near_cities:
    burger = burger.exclude(adress__contains=i).values('title', 'adress')
    kfc = kfc.exclude(adress__contains=i).values('title', 'adress')
    vkusno = vkusno.exclude(adress__contains=i).values('title', 'adress')



print(f'Количество ресторанов "Бургер Кинг" в г. Москва: {len(burger)}')
print(f'Количество ресторанов "KFC" в г. Москва: {len(kfc)}')
print(f'Количество ресторанов "Вкусно — и точка" в г. Москва: {len(vkusno)}')

df = pd.DataFrame({'title': [],
                   'adress': []
    })

for i in [burger, kfc, vkusno]:
    for j in i:
        df.loc[len(df.index)] = {
                'title': j['title'],
                'adress': j['adress']
            }

a = df.groupby(['title']).agg({'title': 'count'}).assign(percentage=lambda x: round(x / x.sum() * 100, 2))
print(f"Количество ресторанов в г. Москва: {df['title'].value_counts().sum()}")
print(a)



