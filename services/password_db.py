import os
import sqlite3

class PasswordDb():
    def __init__(self):
        
        self.db_directory = os.path.expanduser("~")  # Diretório padrão do usuário
        
        self.ocult_folder = os.path.join(self.db_directory, '.cipher_guard')
        if not os.path.exists(self.ocult_folder):
            os.makedirs(self.ocult_folder)

        self.db_path = os.path.join(self.db_directory, '.cipher_guard', 'cipher_guard.db')


        self.connect = sqlite3.connect(self.db_path)
        self.cursor = self.connect.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS password (
                            id INTEGER PRIMARY KEY,
                            label TEXT,
                            value TEXT
                        )''')
        self.connect.commit()

    def insertPassword(self, label, value):
        self.cursor.execute("INSERT INTO password (label, value) VALUES (?, ?)", ( label, value))
        self.connect.commit()

    def removePassword(self, id: int):
        self.cursor.execute("DELETE FROM password WHERE id = ?", (id,))
        self.connect.commit()

    def getAllPasswords(self):
        self.cursor.execute("SELECT * FROM password")
        return self.cursor.fetchall()
        