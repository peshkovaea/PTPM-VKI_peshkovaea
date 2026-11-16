import requests
import bs4

class ForumParser:
    """Парсер каталога смартфонов."""
    
    URL = 'https://sibdroid.ru/catalog/smartfony_samsung/'
    
    # передаю User-Agent 
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36'
    }

    def get_html(self, url=None):
        response = requests.get(url or self.URL, headers=self.HEADERS, timeout=10)
        response.raise_for_status()
        return response.text

    # Этот метод для тестов (передаю ему HTML из файла)
    def parse_html(self, html):
        bs = bs4.BeautifulSoup(html, 'lxml')
        cards = bs.find_all('div', class_='c20-body')
        
        result = []
        for card in cards:
            # ID сообщения (артикул товара)
            sku_tag = card.find('meta', itemprop='sku')
            if not sku_tag:
                continue
            phone_id = int(sku_tag['content'])

            # Логин / Имя (название товара)
            name_tag = card.find('meta', itemprop='name')
            name = name_tag['content'] if name_tag else "Неизвестно"

            # Текст сообщения (цена + рейтинг)
            price_tag = card.find('meta', itemprop='price')
            price = price_tag['content'] + ' ₽' if price_tag else '—'
            
            rating_tag = card.find('a', class_='rv-tile')
            rating = rating_tag.find('b').text if rating_tag else '—'

            message = f"Цена: {price} | Рейтинг: {rating}"

            result.append({
                'id': phone_id,
                'name': name,
                'message': message
            })
        return result

    # скачивает и сразу парсит
    def parse_page(self, url=None):
        html = self.get_html(url)
        return self.parse_html(html)

    # сохранение в БД
    def save_to_db(self, parsed_data, repository):
        saved = 0
        for item in parsed_data:
            try:
                repository.add(item['id'], item['name'], item['message'])
                saved += 1
            except Exception as e:
                print(f"Пропуск ID {item.get('id')}: {e}")
        return saved