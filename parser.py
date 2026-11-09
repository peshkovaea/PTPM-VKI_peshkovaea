import requests
import bs4

response = requests.get('https://sibdroid.ru/catalog/smartfony_samsung/')

bs = bs4.BeautifulSoup(response.text, 'html.parser')

phones = bs.find_all('div', class_='c20-body')
for phone in phones:
    name   = phone.find('span', itemprop='name').text
    price  = phone.find('meta', itemprop='price')['content'] + ' ₽'
    rating = phone.find('a', class_='rv-tile')
    rating = rating.find('b').text if rating else '—'
    print(f"{name} - {price} - {rating}")