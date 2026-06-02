import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import os

# FONT = ctk.CTkFont("Inter", 14, "bold")

root = Path(__file__).resolve().parent
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(os.path.join(root, "Sweetkind.json"))


class LoginScreen(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, title="Login Screen")
        self.grid_columnconfigure(0, weight=1)
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your username...")


class MovieBrowser(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, title="Movie Browser")
        self.grid_columnconfigure(0, weight=1)


class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("streaming service")
        self.geometry("400x220")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = LoginScreen(self)
        self.login_frame.pack()

        self.browse_frame = Brow

    def logged_in(self):
        self.login_frame.pack_forget()
        self.browse_frame.pack()

    def button_callback(self):
        print("hi")


app = StreamingApp()
app.mainloop()
