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
    categories = [{'title': 'Помощь беженцам', 'id': 'makler1e12b1d147c04bd489524ba204553ec5', 'links': ['https://makler.md/ru/assistance-refugees']}, {'title': 'Транспорт', 'id': 'makler06e39e8fb052481ebf00de0e85d25935', 'links': ['https://makler.md/ru/transport']}, {'title': 'Работа и обучение', 'id': 'makler1376b26774ff4033a713d5874232e6d9', 'links': ['https://makler.md/ru/job']}, {'title': 'Услуги', 'id': 'makler93f9779767bc4140814474d228210282', 'links': ['https://makler.md/ru/services']}, {'title': 'Строительство и ремонт', 'id': 'makler514916dd43a345c6804a41075fc99a41', 'links': ['https://makler.md/ru/construction-and-repair']}, {'title': 'Мебель и интерьер', 'id': 'makler6d98c166710a45b4bfff56f3d44a9a4f', 'links': ['https://makler.md/ru/furniture-and-interior']}, {'title': 'Одежда, обувь, аксессуары', 'id': 'maklerc0cd8a2b53f04ba2aeeb68af86893ea6', 'links': ['https://makler.md/ru/clothing-footwear-accessories']}, {'title': 'Все для детей', 'id': 'maklere0236295cc4043bbb5f40d48bf2b06cb', 'links': ['https://makler.md/ru/products-for-children']}, {'title': 'Handmade', 'id': 'makler994baa3e18044091b9ae880c4167da50', 'links': ['https://makler.md/ru/handmade']}, {'title': 'Компьютеры, оргтехника и IT', 'id': 'maklerb58306520a6f4665af3ccbc1d194c513', 'links': ['https://makler.md/ru/computers-and-office-equipment']}, {'title': 'Аудио, видео, фото, ТВ', 'id': 'makler149f68dbb07944c19127df48621fda9d', 'links': ['https://makler.md/ru/audio-photo-video']}, {'title': 'Телефоны и связь', 'id': 'maklerbd07525d257f4bb0b9a01acc6bd17ade', 'links': ['https://makler.md/ru/phones-and-communications']}, {'title': 'Бытовая техника', 'id': 'maklere1ed394bfb7741cf801c5ad4bf942aab', 'links': ['https://makler.md/ru/household-products']}, {'title': 'Оборудование и приборы', 'id': 'maklerf2116d0e69ed4e7a895a3b281759c968', 'links': ['https://makler.md/ru/industrial-and-commercial-equipment']}, {'title': 'Туризм, спорт и отдых', 'id': 'makler5181b325da7343cc9e9fa65b06c490c1', 'links': ['https://makler.md/ru/sport-and-leisure']}, {'title': 'Растения и животные', 'id': 'makler8e383b022f8846d9ad8532c0a00c9936', 'links': ['https://makler.md/ru/plants-and-animals']}, {'title': 'Дачное и сельское хозяйство', 'id': 'makler5bdcfe975c3040828bb2a59f47399e1f', 'links': ['https://makler.md/ru/agribusiness']}, {'title': 'Знакомства', 'id': 'makler77abc95015a64e56abf7e08424ba9c84', 'links': ['https://makler.md/ru/dating']}, {'title': 'Свадьбы, праздники и подарки', 'id': 'makler91c84203559f44efbfba3da042c050be', 'links': ['https://makler.md/ru/weddings-and-celebration']}]
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

                link = lambda: base_link + f'&page={page}' if '?' in base_link else base_link + f'?page={page}'
                resp = requests.get(link(), headers=headers)
                if resp.status_code // 100 != 2:
                    return
                soup = bs4.BeautifulSoup(resp.text, 'lxml')


                while len(contacts) < limit or limit == -1:
                    elements = soup.find('div', {'class': 'ls-detail'})
                    if elements is None:
                        break

                    elements = elements.find_all('article')
                    if elements is None:
                        break
                    
                    for element in elements:
                        if len(contacts) > limit and limit != -1:
                            break

                        try:
                            current_link = 'https://makler.md' + element.find('a', {'class': 'ls-detail_anUrl'})['href']
                            info = self.__parse_current_page(current_link)
                            contacts.append(info)
                            print(len(contacts), 'of', limit, '- Makler')
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
            if len(contacts) > limit and limit != -1:
                break

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


