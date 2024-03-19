import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import csv


result = []

page_count = 1
old_page = 1
url = open('input.txt').readline()
print('Начало')

print('Старт работы')
while True:
    url = url.replace(f'page={old_page}', f'page={page_count}')

    url = url.replace('perPage=12', f'perPage=24')

    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(15)
    page_source = driver.page_source
    driver.close()
    r = requests.get(url).text
    soup = BeautifulSoup(page_source, 'html.parser')

    chekflag = soup.find('div', attrs={'class': 'ui icon header'})

    if chekflag:
        break
    try:
        print(f'Страница {page_count} -- начало парсинга')

        el = soup.findAll('div', attrs={'class':
                                            'six wide computer four wide large screen twelve wide mobile six wide tablet four wide widescreen column CatalogListStyles__CardColumn-sc-1xbpgef-13 eHODa'})

        if len(el) == 0:
            break
        item_dict = {}

        c = 0

        for i in el:
            c += 1
            namecte = i.find('a', attrs={'class': 'ui header CardStyles__MainInfoNameHeader-sc-18miw4v-9 ProductionCardStyles__MainInfoSmallNameHeader-sc-32ykf3-1 hxmdBw flVbdC'})
            link = 'https://zakupki.mos.ru' + namecte['href']
            # print(link)
            img = i.find('div', attrs={'class': 'SquareImage__Image-sc-jhjzcz-0 doIHqg'}).findNext('img')['src']

            cte = ''.join([j for j in namecte['href'] if j.isdigit()])
            name = namecte.findNext('span').text

            price = i.find('div', attrs={'class': 'ui blue header CardStyles__PriceInfoNumber-sc-18miw4v-10 elSNcc'})
            if price:
                price = price.text.replace('&nbsp;', '').replace('\u20bd', '')
            else:
                price = '---'

            # Загрузка фоток
            p = requests.get(img)
            out = open(f"images\\img_{cte}.jpg", "wb")
            out.write(p.content)
            out.close()

            item_dict['img'] = img
            item_dict['link'] = link
            item_dict['cte'] = cte
            item_dict['name'] = name
            item_dict['img_path'] = f"images\\img_{cte}.jpg"
            item_dict['price'] = price
            print(c, link, ' - товар загружен')
            result.append(item_dict)
        print(f'Страница {page_count} завершена')

        old_page = page_count
        page_count += 1

    except TypeError:
        print('Работа завершенна')
        break
    except Exception as ex:
        print('Что-то пошло не так ошибка - ', ex)
        print('Проверте ваше подключение. Может страница не может загрузиться')
        break

f = open('result.csv', 'w', newline='')
writer = csv.writer(f, delimiter=';')
writer.writerow(['Ссылка', 'Изображение', 'Ссылка на изображение', 'СТЕ', 'Наименование товара', 'Цена'])
for data in result:
    writer.writerow([data['link'], data['img_path'], data['img'], data['cte'], data['name'], data['price']])

