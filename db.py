import sqlite3


class SQLiteBooks:
    def __init__(self, db_name='books.db'):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
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

    def add_book(self, user, title, author, year, read=False):
        self.cur.execute('''
            INSERT INTO books (user, title, author, year, read)
            VALUES (?, ?, ?, ?, ?)
        ''', (user, title, author, year, read))
        self.conn.commit()

    def get_read_books(self, user):
        self.cur.execute('SELECT * FROM books WHERE user=? AND read=1', (user,))
        return self.cur.fetchall()

    def mark_book_as_read(self, book_id):
        self.cur.execute('UPDATE books SET read=1 WHERE id=?', (book_id,))
        self.conn.commit()

    def close_connection(self):
        self.cur.close()
        self.conn.close()