from services.setting_db import SettingDb
import random
import string

class GeneratePassword():
    def __init__(self):
        self.setting_db = SettingDb()

    def generate_random_string(self):
        setting = self.setting_db.get_setting()
        length = setting[4]
        use_symbols = setting[1]
        use_numbers = setting[2]
        use_uppercase = setting[3]

        characters = string.ascii_lowercase

        if use_symbols:
            characters += string.punctuation
        if use_numbers:
            characters += string.digits
        if use_uppercase:
            characters += string.ascii_uppercase

        return ''.join(random.choice(characters) for _ in range(length))

    
        