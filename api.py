import requests


def search_books_by_title(title, api_key):
    base_url = 'https://www.googleapis.com/books/v1/volumes?q=flowers+inauthor:keyes&key=' + api_key
    params = {'q': f'intitle:{title}', 'key': api_key}

    try:
        response = requests.get(base_url, params=params)
        data = response.json()

        print(f'{data}')

        if 'items' in data:
            books = data['items']
            return books
        else:
            return None

    except Exception as e:
        print(f'Error occurred: {e}')
        return None