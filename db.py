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
        user_id INTEGER UNIQUE,
        username TEXT NOT NULL UNIQUE,
        full_name TEXT,
        city TEXT,
        office TEXT,
        recall_place TEXT,
        image_bytes TEXT,
        phone TEXT
        )
        ''')
        self.connection.commit()

    def insert_user(self, user_id: int, user_name: str):
        if self._user_in_db(user_id=user_id):
            print(f"User {user_name} already in db")
            return
        self._get_cursor().execute('INSERT INTO Users (user_id, username) VALUES (?, ?)', (user_id, user_name,))
        self._commit()
        print(f"{user_name} - was added in DB")

    def _user_in_db(self, user_id: int) -> bool:
        return self._get_cursor().execute(f"SELECT id from Users WHERE user_id = '{user_id}'").fetchone()

    def save_photo(self, user_id: int, photo: str):
        self._get_cursor().execute("UPDATE Users SET image_bytes = ? WHERE user_id = ?", (photo, user_id))
        self._commit()
        print(f"{user_id} was added photo in DB")

    def save_user_full_name(self, user_id: int, full_name: str):
        self._get_cursor().execute('UPDATE Users SET full_name = ? WHERE user_id = ?', (full_name, user_id))
        self._commit()
        print(f"{user_id} full_name: {full_name} - was added in DB")

    def save_user_city(self, user_id: int, city: str):
        self._get_cursor().execute('UPDATE Users SET city = ? WHERE user_id = ?', (city, user_id))
        self._commit()
        print(f"{user_id} city: {city} - was added in DB")

    def save_user_office(self, user_id: int, office: str):
        self._get_cursor().execute('UPDATE Users SET office = ? WHERE user_id = ?', (office, user_id))
        self._commit()
        print(f"{user_id} office: {office} - was added in DB")

    def save_recall_place(self, user_id: int, recall_place: str):
        self._get_cursor().execute('UPDATE Users SET recall_place = ? WHERE user_id = ?', (recall_place, user_id))
        self._commit()
        print(f"{user_id} recall_place: {recall_place} - was added in DB")

    def save_user_phone(self, user_id: int, phone: str):
        self._get_cursor().execute('UPDATE Users SET phone = ? WHERE user_id = ?', (phone, user_id))
        self._commit()
        print(f"{user_id} phone {phone} - was added in DB")

    def delete_user(self, user_id: int):
        self._get_cursor().execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
        self._commit()
        print(f"{user_id} was deleted from DB")

    def get_user(self, user_id):
        return self._get_cursor().execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()
