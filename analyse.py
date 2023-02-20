import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "restaurants.settings")
django.setup()

import pandas as pd

from django.db.models import Q
from list_rest.models import Restaurant


# Ограничение по названию и вхождению только в г. Москва, т.к. в модель попали лишние
burger = Restaurant.objects.filter(Q(title='Бургер Кинг') & ~Q(adress__contains='область')).values('title', 'adress', 'lat', 'lon')
kfc = Restaurant.objects.filter(Q(title='KFC') & ~Q(adress__contains='область')).values('title', 'adress', 'lat', 'lon')
vkusno = Restaurant.objects.filter(Q(title='Вкусно — и точка') & ~Q(adress__contains='область')).values('title', 'adress', 'lat', 'lon')


# print(f'Количество ресторанов "Бургер Кинг" в г. Москва: {len(burger)}')
# print(f'Количество ресторанов "KFC" в г. Москва: {len(kfc)}')
# print(f'Количество ресторанов "Вкусно — и точка" в г. Москва: {len(vkusno)}')

df = pd.DataFrame({'title': [],
                   'adress': [],
                   'lat': [],
                   'lon': []
    })

for i in [burger, kfc, vkusno]:
    for j in i:
        df.loc[len(df.index)] = {
                'title': j['title'],
                'adress': j['adress'],
                'lat': j['lat'],
                'lon': j['lon']
            }

a = df.groupby(['title']).agg({'title': 'count'}).assign(percentage=lambda x: round(x / x.sum() * 100, 2))
print(f"Количество ресторанов в г. Москва: {df['title'].value_counts().sum()}")
print(a)



