import requests


def search_books_by_title(title, api_key='AIzaSyC2GktczVkMHkhg84_aoKXj4I3xwsO9D54'):
    base_url = f'https://www.googleapis.com/books/v1/volumes?q={title}+intitle:keyes&key={api_key}'

    payload = {}
    headers = {}

    try:
        response = requests.request("GET", base_url, headers=headers, data=payload)
        data = response.json()

        books = []
        counter = 1
        for item in data["items"]:
            volume_info = item.get("volumeInfo", {})
            title = volume_info.get("title")
            authors = volume_info.get("authors")
            published_date = volume_info.get("publishedDate")

            #TODO выводить только уникальные книги по названию
            if title and authors and published_date:  # Проверяем, что все необходимые поля не пустые
                book_info = {
                    "id_message": counter,
                    "id": item["id"],
                    "title": title,
                    "author": authors[0],
                    "year": published_date
                }
                books.append(book_info)

            counter += 1

        return books

    except Exception as e:
        print(f'Error occurred: {e}')
        return None


def get_newest_books(api_key='AIzaSyC2GktczVkMHkhg84_aoKXj4I3xwsO9D54'):
    # URL для запроса к Google Books API
    url = 'https://www.googleapis.com/books/v1/volumes'

    # Параметры запроса
    params = {
        'q': 'subject:fiction',  # Тема книги (может быть любой)
        'orderBy': 'newest',  # Сортировка по дате публикации (новые книги)
        'maxResults': 10  # Максимальное количество результатов (в данном случае - 10 книг)
        # 'langRestrict': 'ru'  # Ограничение результатов поиска на русский язык
    }

    try:
        # Выполнение запроса и получение ответа
        response = requests.get(url, params=params)

        books = []

        # Проверка успешности запроса
        if response.status_code == 200:
            # Получение данных о книгах из JSON-ответа
            data = response.json()

            counter = 1
            for item in data["items"]:
                volume_info = item.get("volumeInfo", {})
                title = volume_info.get("title")
                authors = volume_info.get("authors")
                published_date = volume_info.get("publishedDate")

                #TODO выводить только уникальные книги по названию
                if title and authors and published_date:  # Проверяем, что все необходимые поля не пустые
                    book_info = {
                        "id_message": counter,
                        "id": item["id"],
                        "title": title,
                        "author": authors[0],
                        "year": published_date
                    }
                    books.append(book_info)

                counter += 1

        return books

    except Exception as e:
        print(f'Error occurred: {e}')
        return None
