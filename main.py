from tkinter import messagebox
import customtkinter
from gui.generate_password_frame import GeneratePasswordFrame
from gui.list_password_frame import ListPasswordFrame
from services.setting_db import SettingDb

# --- CUSTOM APPEARANCE ---
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("green")

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Cipher Guard")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        try:
            SettingDb()

            self.list_password_frame = ListPasswordFrame(master=self, label_text="List Passwords")
            self.list_password_frame.grid(row=1, column=0, padx=10, pady=(0,10), sticky="nsew")

            self.generate_password_frame = GeneratePasswordFrame(master=self, list_password_frame=self.list_password_frame)
            self.generate_password_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export data: {str(e)}")

        

app = App()
app.mainloop()