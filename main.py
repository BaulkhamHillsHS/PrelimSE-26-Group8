import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import os

# FONT = ctk.CTkFont("Inter", 14, "bold")

root = Path(__file__).resolve().parent
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(os.path.join(root, "Sweetkind.json"))


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, switch_function):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.switch_function = switch_function
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your username...")
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_submit)
        
        self.name_entry.pack()
        self.login_button.pack()
        
    def login_submit(self):
        self.switch_function(self.name_entry.get())

class MovieBrowser(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)

class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("streaming service")
        self.geometry("400x220")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = LoginScreen(self, switch_function=self.log_in_switch)
        self.login_frame.pack()

        self.browse_frame = MovieBrowser(self)

    def log_in_switch(self, user):
        print(f"Logging in as {user}")
        self.login_frame.pack_forget()
        self.browse_frame.pack()

    def button_callback(self):
        print("hi")


app = StreamingApp()
app.mainloop()
