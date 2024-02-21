import shutil
from tkinter import messagebox
from PIL import Image
from customtkinter import *
from services.setting_db import SettingDb

class ToplevelWindow(CTkToplevel):
    def __init__(self, *args, list_password_frame, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Settings")

        self.setting_db = SettingDb()
        self.list_password_frame = list_password_frame

        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.parent_directory = os.path.dirname(self.current_path)

        self.export_image_path = os.path.join(self.parent_directory, "assets", "export.png")
        self.import_image_path = os.path.join(self.parent_directory, "assets", "import.png")
        self.save_image_path = os.path.join(self.parent_directory, "assets", "save.png")

        self.icon_export = CTkImage(dark_image=Image.open(self.export_image_path))
        self.icon_import = CTkImage(dark_image=Image.open(self.import_image_path))
        self.icon_save = CTkImage(dark_image=Image.open(self.save_image_path))

        self.label = CTkLabel(self, text="Password length", font=("", 10, "bold"))
        self.label.grid(row=0, column=0,padx=20, pady=(20,0), sticky="w")

        self.slider_length = CTkSlider(self, from_=5, to=25, progress_color="transparent", command=self.slider_event)
        self.slider_length.grid(row=1, column=0, padx=20, pady=20)

        self.value_slider= CTkLabel(self, text="")
        self.value_slider.grid(row=1, column=1, padx=20, pady=20 )

        self.checkbox_symbols = CTkCheckBox(self, text="Special symbols", font=("", 10, "bold"))
        self.checkbox_symbols.grid(row=2, column=0,padx=20, pady=20, sticky="w")

        self.checkbox_numbers = CTkCheckBox(self, text="Numbers",  font=("", 10, "bold"))
        self.checkbox_numbers.grid(row=3, column=0,padx=20, pady=20, sticky="w")

        self.checkbox_uppercase = CTkCheckBox(self, text="Uppercase", font=("", 10, "bold"))
        self.checkbox_uppercase.grid(row=4, column=0,padx=20, pady=20, sticky="w")

        self.button_save = CTkButton(self, text="Save", text_color="#fff", image=self.icon_save, command=self.save_setting)
        self.button_save.grid(row=5, column=0, padx=20, pady=20, sticky="nsew")

        self.button_export = CTkButton(self, text="Export Data", text_color="#fff", image=self.icon_export, command=self.export_passwords)
        self.button_export.grid(row=5, column=1, padx=0, pady=20, sticky="nsew")

        self.button_import = CTkButton(self, text="Import Data", text_color="#fff", image=self.icon_import, command=self.import_passwords)
        self.button_import.grid(row=5, column=2, padx=20, pady=20, sticky="nsew")

        self.set_values()

    def save_setting(self):
        value_slider = int(self.slider_length.get())
        value_checkbox_symbols = self.checkbox_symbols.get()
        value_checkbox_numbers = self.checkbox_numbers.get()
        value_checkbox_uppercase = self.checkbox_uppercase.get()

        self.setting_db.update_setting(value_checkbox_symbols, value_checkbox_numbers, value_checkbox_uppercase, value_slider)

        self.destroy()

    def set_values(self):
        setting = self.setting_db.get_setting()
        
        self.slider_length.set(setting[4])
        self.value_slider.configure(text=setting[4])

        self.checkbox_symbols.select() if bool(setting[1]) else self.checkbox_symbols.deselect()
        self.checkbox_numbers.select() if bool(setting[2]) else self.checkbox_numbers.deselect()
        self.checkbox_uppercase.select() if bool(setting[3]) else self.checkbox_uppercase.deselect()


    def export_passwords(self):
        try:
            db_path = "cipher_guard.db"
            export_path = filedialog.asksaveasfilename(defaultextension=".db")
            shutil.copy(db_path, export_path)

            messagebox.showinfo("Success", "Data exported successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")
        

    def import_passwords(self):
        try:
            db_path = "cipher_guard.db"
            import_path = filedialog.askopenfilename(filetypes=[("Database Files", "*.db")])
            if import_path:
                shutil.copy(import_path, db_path)
                self.list_password_frame.render_list()
                messagebox.showinfo("Success", "Data imported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to import data: {str(e)}")
        

    def slider_event(self, value):
        value_parse = int(value)
        self.value_slider.configure(text=value_parse)