import os
import sqlite3

class SettingDb():
    def __init__(self):

        self.db_directory = os.path.expanduser("~")

        self.ocult_folder = os.path.join(self.db_directory, '.cipher_guard')
        if not os.path.exists(self.ocult_folder):
            os.makedirs(self.ocult_folder)

          # Diretório padrão do usuário
        self.db_path = os.path.join(self.db_directory, '.cipher_guard', 'cipher_guard.db')


        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS setting (
                            id INTEGER PRIMARY KEY,
                            special_symbols INTEGER CHECK(special_symbols IN (0, 1)),
                            numbers INTEGER CHECK(numbers IN (0, 1)),
                            uppercase INTEGER CHECK(numbers IN (0, 1)),
                            password_length INTEGER CHECK(password_length >= 5 AND password_length <= 25)
                        )''')
        
        self.cursor.execute("SELECT COUNT(*) FROM setting")

        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute("INSERT INTO setting (special_symbols, numbers, uppercase, password_length) VALUES (0, 0, 0, 10)")
        
        self.connect.commit()

    def update_setting(self, special_symbols, numbers, uppercase, password_length):
        self.cursor.execute("UPDATE setting SET special_symbols=?, numbers=?, uppercase=?, password_length=?", (special_symbols, numbers, uppercase, password_length))
        self.connect.commit()

    def get_setting(self):
        self.cursor.execute("SELECT * FROM setting")
        return self.cursor.fetchone()
        