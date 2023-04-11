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
    categories = [{'title': 'Помощь беженцам', 'id': 'maklerf6a66ca4c1884aedacfbd2e05b532353', 'links': ['https://makler.md//ru/assistance-refugees']}, {'title': 'Транспорт', 'id': 'makler77c2767eb95f4ab38c42e8398ff5a80d', 'links': ['https://makler.md//ru/transport']}, {'title': 'Работа и обучение', 'id': 'makler097072c994034c7299d24f4347627384', 'links': ['https://makler.md//ru/job']}, {'title': 'Услуги', 'id': 'makler3d13bb1dc93f4a8d9781b4d728211979', 'links': ['https://makler.md//ru/services']}, {'title': 'Строительство и ремонт', 'id': 'maklera579e8a48a444f25940ff7847345aa5f', 'links': ['https://makler.md//ru/construction-and-repair']}, {'title': 'Мебель и интерьер', 'id': 'makler78dc3c92149240688a873ddff4127742', 'links': ['https://makler.md//ru/furniture-and-interior']}, {'title': 'Одежда, обувь, аксессуары', 'id': 'maklerfb7dd92ddd214d3aad8230145ce0fdab', 'links': ['https://makler.md//ru/clothing-footwear-accessories']}, {'title': 'Все для детей', 'id': 'maklere7d201cfe8ab4df396b5dac8e39ee6f8', 'links': ['https://makler.md//ru/products-for-children']}, {'title': 'Handmade', 'id': 'makler9f9bd724371c48c1abff303769c269d2', 'links': ['https://makler.md//ru/handmade']}, {'title': 'Компьютеры, оргтехника и IT', 'id': 'makler7810004a671844558138a4e38cd9d41d', 'links': ['https://makler.md//ru/computers-and-office-equipment']}, {'title': 'Аудио, видео, фото, ТВ', 'id': 'makler297f9864b10b4c4bb33745e3bc0f5ae4', 'links': ['https://makler.md//ru/audio-photo-video']}, {'title': 'Телефоны и связь', 'id': 'makler6d9f75f43a434f0f8ee426f856a42659', 'links': ['https://makler.md//ru/phones-and-communications']}, {'title': 'Бытовая техника', 'id': 'makler4bfb1758bf234f8f945fc81b554921ec', 'links': ['https://makler.md//ru/household-products']}, {'title': 'Оборудование и приборы', 'id': 'makler1746777ec20646b7a941c5b95b5484d6', 'links': ['https://makler.md//ru/industrial-and-commercial-equipment']}, {'title': 'Туризм, спорт и отдых', 'id': 'maklerbc24520c557a4e71b9fa33061c55ca33', 'links': ['https://makler.md//ru/sport-and-leisure']}, {'title': 'Растения и животные', 'id': 'makler5696b18bdf0f4b2daced6c2ab2dea205', 'links': ['https://makler.md//ru/plants-and-animals']}, {'title': 'Дачное и сельское хозяйство', 'id': 'maklerd4a512cf5fcd4c00b2543eef9e0ad915', 'links': ['https://makler.md//ru/agribusiness']}, {'title': 'Знакомства', 'id': 'makler855f0d2f49474f5db4564b07de7d1354', 'links': ['https://makler.md//ru/dating']}, {'title': 'Свадьбы, праздники и подарки', 'id': 'makler012124df24fa4ceba628effa877b4377', 'links': ['https://makler.md//ru/weddings-and-celebration']}]

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


