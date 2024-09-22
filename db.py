import os
import sqlite3

DATABASE_PATH = "db/kam_db.db"


class Database:
    def __init__(self):

        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

        self.connection = sqlite3.connect(
            DATABASE_PATH, check_same_thread=False)
        self._create_users_table()

    def _get_cursor(self):
        return self.connection.cursor()

    def close(self):
        self.connection.close()

    def _commit(self):
        self.connection.commit()

    def _create_users_table(self):
        cursor = self._get_cursor()

        # Проверка существования таблицы Users
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Users';")
        table_exists = cursor.fetchone()

        if table_exists:
            # Проверка существования поля bank
            cursor.execute("PRAGMA table_info(Users);")
            columns = cursor.fetchall()
            column_names = [column[1] for column in columns]

            if 'bank' not in column_names:
                # Добавление поля bank, если оно не существует
                cursor.execute("ALTER TABLE Users ADD COLUMN bank TEXT;")
                self._commit()
                print("Поле 'bank' добавлено в таблицу 'Users'")
        else:
            # Создание таблицы Users, если она не существует
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            user_id INTEGER UNIQUE,
            username TEXT NOT NULL UNIQUE,
            full_name TEXT,
            city TEXT,
            office TEXT,
            recall_place TEXT,
            image_bytes TEXT,
            phone TEXT,
            bank TEXT
            )
            ''')
            self._commit()

    def insert_user(self, user_id: int, user_name: str):
        if self.user_in_db(user_id=user_id):
            print(f"User {user_name} already in db")
            return
        self._get_cursor().execute(
            'INSERT INTO Users (user_id, username) VALUES (?, ?)', (user_id, user_name,))
        self._commit()
        print(f"{user_name} - was added in DB")

    def user_in_db(self, user_id: int) -> bool:
        return self._get_cursor().execute(f"SELECT id from Users WHERE user_id = '{user_id}'").fetchone()

    def save_photo(self, user_id: int, photo: str):
        self._get_cursor().execute(
            "UPDATE Users SET image_bytes = ? WHERE user_id = ?", (photo, user_id))
        self._commit()
        print(f"{user_id} was added photo in DB")

    def save_user_full_name(self, user_id: int, full_name: str):
        self._get_cursor().execute(
            'UPDATE Users SET full_name = ? WHERE user_id = ?', (full_name, user_id))
        self._commit()
        print(f"{user_id} full_name: {full_name} - was added in DB")

    def save_user_city(self, user_id: int, city: str):
        self._get_cursor().execute(
            'UPDATE Users SET city = ? WHERE user_id = ?', (city, user_id))
        self._commit()
        print(f"{user_id} city: {city} - was added in DB")

    def save_user_office(self, user_id: int, office: str):
        self._get_cursor().execute(
            'UPDATE Users SET office = ? WHERE user_id = ?', (office, user_id))
        self._commit()
        print(f"{user_id} office: {office} - was added in DB")

    def save_recall_place(self, user_id: int, recall_place: str):
        self._get_cursor().execute(
            'UPDATE Users SET recall_place = ? WHERE user_id = ?', (recall_place, user_id))
        self._commit()
        print(f"{user_id} recall_place: {recall_place} - was added in DB")

    def save_user_phone(self, user_id: int, phone: str):
        self._get_cursor().execute(
            'UPDATE Users SET phone = ? WHERE user_id = ?', (phone, user_id))
        self._commit()
        print(f"{user_id} phone {phone} - was added in DB")

    def save_user_bank(self, user_id: int, bank: str):
        self._get_cursor().execute(
            'UPDATE Users SET bank = ? WHERE user_id = ?', (bank, user_id))
        self._commit()
        print(f"{user_id} bank {bank} - was added in DB")

    def delete_user(self, user_id: int):
        self._get_cursor().execute('DELETE FROM Users WHERE user_id = ?', (user_id,))
        self._commit()
        print(f"{user_id} was deleted from DB")

    def get_user(self, user_id):
        return self._get_cursor().execute(f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()
