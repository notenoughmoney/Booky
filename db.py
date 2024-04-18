import sqlite3
from collections import Counter


class SQLiteBooks:
    def __init__(self, db_name='books.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table_read_books()
        self.create_table_users()

    def create_table_read_books(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY,
                user TEXT,
                title TEXT,
                author TEXT,
                year TEXT,
                read BOOLEAN
            )
        ''')
        self.conn.commit()

    def create_table_users(self):
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                user TEXT,
                status TEXT
            )
        ''')
        self.conn.commit()

    def make_vip(self, user):
        self.cur.execute('''
            INSERT INTO users (user, status)
            VALUES (?, ?)
        ''', (user, "VIP"))
        self.conn.commit()

    def get_user_status(self, user):
        self.cur.execute('SELECT status FROM users WHERE user=?', (user,))
        status = self.cur.fetchone()
        if status:
            return status[0]  # Возвращаем статус, если он был найден
        else:
            return None  # Возвращаем None, если пользователь не найден

    def add_book(self, user, title, author, year, read=True):
        self.cur.execute('''
            INSERT INTO books (user, title, author, year, read)
            VALUES (?, ?, ?, ?, ?)
        ''', (user, title, author, year, read))
        self.conn.commit()

    def get_read_books(self, user):
        self.cur.execute('SELECT * FROM books WHERE user=? AND read=1', (user,))
        rows = self.cur.fetchall()

        # Получаем имена столбцов из описания таблицы
        columns = [col[0] for col in self.cur.description]

        # Преобразуем списки кортежей в список словарей
        books_list = []
        for row in rows:
            book_dict = dict(zip(columns, row))
            books_list.append(book_dict)

        return books_list

    def get_read_books_count(self, user):
        self.cur.execute('SELECT COUNT(*) FROM books WHERE user=? AND read=1', (user,))
        count = self.cur.fetchone()[0]
        return count

    def mark_book_as_read(self, book_id):
        self.cur.execute('UPDATE books SET read=1 WHERE id=?', (book_id,))
        self.conn.commit()

    def get_recommendations(self, user):
        # Получаем все прочитанные книги, кроме тех, которые прочитал пользователь
        self.cur.execute('''
            SELECT id, title, author, year FROM books
            WHERE user != ? AND read=1
        ''', (user,))
        rows = self.cur.fetchall()

        # Получаем книги, которые прочитал пользователь
        user_books = self.get_read_books(user)

        # Создаем список всех прочитанных книг другими пользователями, кроме книг пользователя user
        all_books = [{'id': row[0], 'title': row[1], 'author': row[2], 'year': row[3]} for row in rows]

        # Получаем книги, которые прочитал пользователь
        user_books_ids = [book['id'] for book in user_books]

        # Формируем список рекомендаций в нужном формате, исключая книги, которые пользователь уже прочитал
        recommendations_list = []
        counter = 1
        for book in all_books:
            if book['id'] not in user_books_ids:
                book_info = {
                    "id_message": counter,
                    "id": book['id'],
                    "title": book['title'],
                    "author": book['author'],
                    "year": book['year']
                }
                recommendations_list.append(book_info)
                counter += 1

        return recommendations_list

    def close_connection(self):
        self.cur.close()
        self.conn.close()
