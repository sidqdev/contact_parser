import requests
import bs4
from uuid import uuid4

base = 'https://makler.md/'

soup = bs4.BeautifulSoup(requests.get('https://makler.md/ru').text, 'lxml')

soup = soup.find('div', {'class': 'col-left'})
soup = soup.find('nav')
soup = soup.find_all('a', {'class': 'catMenu'})

all_items = list()

for i in soup:
    title = i.text.strip()
    links = [base + i['href']]
    id = 'makler' + uuid4().hex

    all_items.append(
        {
            "title": title,
            "id": id,
            "links": links
        }
    )

print(all_items)