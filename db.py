import sqlite3


class Database:
    def __init__(self):
        self.connection = sqlite3.connect('kam_db.db', check_same_thread=False)
        self._create_users_table()

    def _get_cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()

    def _commit(self):
        self.connection.commit()

    def _create_users_table(self):
        self._get_cursor().execute('''
        CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        prone INTEGER
        )
        ''')
        self.connection.commit()

    def insert_user(self, user_name: str):
        if self._user_in_db(user_name=user_name):
            print(f"User {user_name} already in db")
            return
        self._get_cursor().execute('INSERT INTO Users (username) VALUES (?)', (user_name,))
        self._commit()
        print(f"{user_name} - was added in DB")

    def _user_in_db(self, user_name: str) -> bool:
        return self._get_cursor().execute(f"SELECT id from Users WHERE username = '{user_name}'").fetchone()

    def save_user_phone(self, phone: int, user_name: str):
        self._get_cursor().execute('UPDATE Users SET prone = ? WHERE username = ?', (phone, user_name))
        self._commit()
        print(f"{user_name} phone {phone} - was added in DB")
