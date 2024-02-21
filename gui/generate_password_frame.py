from PIL import Image
from customtkinter import *
import pyperclip
from gui.settings_toplevel import ToplevelWindow
from gui.list_password_frame import ListPasswordFrame
from services.password_db import PasswordDb
from utils.generate_password import GeneratePassword

class GeneratePasswordFrame(CTkFrame):
    def __init__(self, master, list_password_frame, **kwargs):
        super().__init__(master, **kwargs)

        self.list_password_frame = list_password_frame
        self.password_db = PasswordDb()
        self.generate_password = GeneratePassword()
        self.settings_toplevel = None

        # Load images
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.parent_directory = os.path.dirname(self.current_path)

        self.settings_image_path = os.path.join(self.parent_directory, "assets", "settings.png")
        self.password_image_path = os.path.join(self.parent_directory, "assets", "password.png")
       
        self.icon_settings = CTkImage(dark_image=Image.open(self.settings_image_path))
        self.icon_generate = CTkImage(dark_image=Image.open(self.password_image_path))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # add widgets onto the frame...
        self.input = CTkEntry(self, placeholder_text="Enter password label")
        self.input.bind("<KeyRelease>", self.on_input_change)
        self.input.grid(row=0, column=0, columnspan=3, padx=10, pady=10,sticky="ew")

        self.label = CTkLabel(self, text="**********",font=("Consolas", 24, "bold"), cursor="hand2")
        self.label.bind("<Button-1>", self.copy_label_text)
        
        self.button_generate = CTkButton(self, text="Generate", text_color="#fff", image=self.icon_generate,command=self.on_click_button_generate, state=DISABLED)
        self.button_generate.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

        self.button_settings = CTkButton(self, text="Settings", text_color="#fff", image=self.icon_settings, command=self.on_click_button_setting)
        self.button_settings.grid(row=1, column=1, padx=(0, 10), pady=(0, 10), sticky="nsew")

    def on_click_button_generate(self):
        data = self.generate_password.generate_random_string()
        inputValue = self.input.get()
        
        self.password_db.insertPassword(label=inputValue, value=data)
        self.list_password_frame.render_list()
        self.label.configure(text=data)
        self.label.grid(row=2, column=0, padx=20, pady=60, sticky="nsew", columnspan=2)

    def on_click_button_setting(self):
        if self.settings_toplevel is None or not self.settings_toplevel.winfo_exists():
            self.settings_toplevel = ToplevelWindow(self, list_password_frame=self.list_password_frame)  # create window if its None or destroyed
        else:
            self.settings_toplevel.focus() 

    def on_input_change(self, _):
        inputValue = self.input.get()
        
        if inputValue.strip():
            self.button_generate.configure(state=NORMAL)
        else:
            self.button_generate.configure(state=DISABLED)

    def copy_label_text(self, event):
        text = self.label.cget("text")
        pyperclip.copy(text) 
        self.label.configure(text="Copied password!") 
        self.label.after(1000, lambda: self.label.configure(text=text))