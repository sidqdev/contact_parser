import requests
import bs4

base = 'https://m.999.md'
soup = bs4.BeautifulSoup(requests.get(input()).text, 'lxml')

soup = soup.find('ul', {"class": "category-page__subcategories"})

links = soup.find_all('a')

links = [base + x['href'] for x in links]

print(links)