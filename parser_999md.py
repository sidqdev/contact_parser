import requests
import bs4
from telebot import TeleBot
from threading import Thread
import os
from uuid import uuid4
import xlsxwriter
import time


class Parser999md:
    def __init__(self, bot: TeleBot) -> None:
        self.bot: TeleBot = bot

    categories = [
        {"title": "Недвижемость", "id": "999_nedviga", "links": [
            'https://m.999.md/ru/list/real-estate/apartments-and-rooms',
            'https://m.999.md/ru/list/real-estate/house-and-garden',
            'https://m.999.md/ru/list/real-estate/land',
            'https://m.999.md/ru/list/real-estate/commercial-real-estate',
            'https://m.999.md/ru/list/real-estate/real-estate-abroad'
        ]},
        {
            "title": "Техника", "id": "999_tech", "links": [
                'https://m.999.md/ru/list/phone-and-communication/mobile-phones',
                'https://m.999.md/ru/list/phone-and-communication/charger-and-batteries',
                'https://m.999.md/ru/list/phone-and-communication/miscellaneous',
                'https://m.999.md/ru/list/phone-and-communication/gadget',
                'https://m.999.md/ru/list/phone-and-communication/service-and-repair-of-telephones',
            ]
        }
    ]

    def get_link_by_id(self, id: str):
        for i in self.categories:
            if id == i.get('id'):
                return i.get('links')

    def get_categories_for_markup(self):
        return [
            {"text": x.get('title'), "callback_data": x.get('id')}
            for x in self.categories
        ]

    def check_category_id(self, id: str):
        for i in self.categories:
            if id == i.get('id'):
                return True
        return False

    def check_link(self, link: str):
        return link.startswith('https://m.999.md/ru/list')

    def parse(self, links: list, limit: int, chat_id: int) -> bool:
        Thread(target=self.__parse, args=(links, limit, chat_id)).start()
        return True
    
    def remove_duplicates_by_phone(self, items: list) -> list:
        a = list()
        b = list()
        for i in items:
            if i[1] not in b:
                a.append(i)
                b.append(i[1])
        return a

    
    def __parse(self, links: list, limit: int, chat_id: int):
        contacts = list()
        for link in links:
            try:
                base_link = link
                page = 1

                link = lambda: base_link + f'&page={page}' if '?' in base_link else base_link + f'?page={page}'
                resp = requests.get(link())
                if resp.status_code // 100 != 2:
                    return
                soup = bs4.BeautifulSoup(resp.text, 'lxml')        


                while len(contacts) < limit or limit == -1:
                    elements = soup.find('ul', {'class': 'block-items is-photo-view'})
                    if elements is None:
                        break

                    elements = elements.find_all('li', {'class': 'block-items__item'})
                    if elements is None:
                        break

                    for element in elements:
                        if len(contacts) > limit and limit != -1:
                            break
                        try:
                            current_link = 'https://m.999.md' + element.find('a', {'class': 'block-items__item__link js-item-ad'})['href']
                            
                            info = self.__parse_current_page(current_link)
                            print(info)
                            contacts.append(info)
                        except:
                            pass
                        finally:
                            time.sleep(1)
                        
                        contacts = self.remove_duplicates_by_phone(contacts)
                    print(len(contacts))
                    if len(contacts) > limit and limit != -1:
                        break
                    
                    try:
                        is_next = soup.find('a', {'class': 'block-nav__next'})['href']
                        if is_next is None:
                            break
                    except:
                        break

                    page += 1
                    resp = requests.get(link())
                    if resp.status_code // 100 != 2:
                        break
                    soup = bs4.BeautifulSoup(resp.text, 'lxml') 
            except Exception as e:
                print(e)  
        
        filename = uuid4().hex + '.xlsx'
        filename = f"{base_link.split('/')[-1]}_{limit}_{filename}"
        workbook = xlsxwriter.Workbook(filename)
        worksheet = workbook.add_worksheet()
        contacts = [('Имя', 'Номер телефона')] + contacts
        
        row = 0
        col = 0

        for item, cost in contacts:
            worksheet.write(row, col, item)
            worksheet.write(row, col+1, cost)
            row += 1

        workbook.close()

        f = open(filename, 'rb')

        self.bot.send_document(chat_id, f)
        os.remove(filename)

    def __parse_current_page(self, link: str):
        resp = requests.get(link)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, 'lxml')

        contacts = soup.find('div', {'class': 'item-page__author-info'})

        name = contacts.find('a', {'class': 'item-page__author-info__item_user'}).text.strip()
        phone = contacts.find('a', {'class': 'item-page__author-info__item_phone'})['href'].split(':')[-1].strip()
        
        while '  ' in name:
            name = name.replace('  ', ' ')
        return (name, phone)

