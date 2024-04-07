import json

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
