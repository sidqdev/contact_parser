import requests
import bs4
from telebot import TeleBot
from threading import Thread
import os
from uuid import uuid4
import xlsxwriter
import time


headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

class ParserMakler:
    categories = [
        {"title": "Недвижемость", "id": "makler_nedviga", "links": [
            'https://makler.md/ru/real-estate/real-estate-for-sale/apartments-for-sale',
            'https://makler.md/ru/real-estate/real-estate-for-rent/apartments-for-rent',
            'https://makler.md/ru/real-estate/real-estate-for-sale/houses-for-sale',
            'https://makler.md/ru/real-estate/real-estate-for-rent/houses-for-rent',
            'https://makler.md/ru/real-estate/real-estate-for-sale/premises-for-sale',
            'https://makler.md/ru/real-estate/real-estate-for-rent/premises-for-rent',
            'https://makler.md/ru/real-estate/real-estate-for-sale/plots-for-sale',
        ]},
        {
            "title": "Техника", "id": "makler_tech", "links": [
                'https://makler.md/ru/computers-and-office-equipment',
                'https://makler.md/ru/audio-photo-video',
                'https://makler.md/ru/phones-and-communications',
                'https://makler.md/ru/household-products',
                'https://makler.md/ru/industrial-and-commercial-equipment',
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

    def __init__(self, bot: TeleBot) -> None:
        self.bot: TeleBot = bot

    def check_link(self, link: str):
        return link.startswith('https://makler.md/ru')

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
                page = 0

                print(1)
                link = lambda: base_link + f'&page={page}' if '?' in base_link else base_link + f'?page={page}'
                resp = requests.get(link(), headers=headers)
                if resp.status_code // 100 != 2:
                    return
                soup = bs4.BeautifulSoup(resp.text, 'lxml')


                while len(contacts) < limit or limit == -1:
                    print(1)
                    elements = soup.find('div', {'class': 'ls-detail'})
                    if elements is None:
                        break

                    elements = elements.find_all('article')
                    if elements is None:
                        break
                    
                    print(2)
                    for element in elements:
                        if len(contacts) > limit and limit != -1:
                            break

                        try:
                            current_link = 'https://makler.md' + element.find('a', {'class': 'ls-detail_anUrl'})['href']
                            print(current_link)
                            info = self.__parse_current_page(current_link)
                            print(info)
                            contacts.append(info)
                        except:
                            pass
                        finally:
                            time.sleep(3)
                        
                        contacts = self.remove_duplicates_by_phone(contacts)
                        
                    if len(contacts) > limit and limit != -1:
                        break

                    page += 1
                    resp = requests.get(link(), headers=headers)
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
        resp = requests.get(link, headers=headers)
        resp.raise_for_status()
        soup = bs4.BeautifulSoup(resp.text, 'lxml')

        name = soup.find('a', {'class': 'item_sipmleUser'}).text.strip()
        phone = soup.find('li', {'itemprop': 'telephone'}).text.strip()
        
        while '  ' in name:
            name = name.replace('  ', ' ')

        while ' ' in phone:
            phone = phone.replace(' ', '')
        return (name, phone)


