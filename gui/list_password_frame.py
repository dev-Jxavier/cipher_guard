from customtkinter import *
import os
from PIL import Image
import pyperclip
from services.password_db import PasswordDb

class ListPasswordFrame(CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.password_db = PasswordDb()

        # Load images
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        self.parent_directory = os.path.dirname(self.current_path)
        self.delete_image_path = os.path.join(self.parent_directory, "assets", "delete.png")

        self.icon_delete = CTkImage(dark_image=Image.open(self.delete_image_path))

        self.bind_all("<Button-4>", lambda e: self._parent_canvas.yview("scroll", -1, "units"))
        self.bind_all("<Button-5>", lambda e: self._parent_canvas.yview("scroll", 1, "units"))

        self.render_list()

    def render_list(self):
        for widget in self.winfo_children():
            widget.destroy()

        values = self.password_db.getAllPasswords()

        for i, value in enumerate(values):
            label = CTkLabel(self, text="{0}: {1}".format(value[1], value[2]), justify="left", cursor="hand2")
            label.bind("<Button-1>", lambda event, label=label, password=value[2]: self.copy_label_text(label, password))
            label.grid(row=i, column=1, padx=10, pady=(10, 0), sticky="w")

            button_delete = CTkButton(self, text="", image=self.icon_delete, fg_color="transparent", hover_color="#dc2f02", width=2)
            button_delete.bind("<Button-1>", lambda event, id=value[0]: self.delete_password(id))
            button_delete.grid(row=i, column=0, pady=(10, 0))

    def copy_label_text(self, label, value):
        pyperclip.copy(value)
        original_text = label.cget("text")
        label.configure(text="Copied password!")
        label.after(1500, lambda: label.configure(text=original_text))

    def delete_password(self, id: int): 
        self.password_db.removePassword(id)
        self.render_list()