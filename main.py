import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import os

#FONT = ctk.CTkFont("Inter", 14, "bold")

root = Path(__file__).resolve().parent
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(os.path.join(root, "Sweetkind.json"))

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, title="Login Screen")
        self.grid_columnconfigure(0, weight=1)
    

class MyScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []

        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes
    

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("streaming service")
        self.geometry("400x220")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        values = ["value 1", "value 2", "value 3", "value 4", "value 5", "value 6"]
        self.scrollable_checkbox_frame = MyScrollableCheckboxFrame(self, title="Values", values=values)
        self.scrollable_checkbox_frame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")

        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=3, column=0, padx=10, pady=10, sticky="ew", columnspan=2)

    def button_callback(self):
        print("hi")

app = App()
app.mainloop()