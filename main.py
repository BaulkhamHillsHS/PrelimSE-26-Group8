from PIL import Image
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import os

FONT = ("Inter", 14, "bold")

root = Path(__file__).resolve().parent
logo_path = os.path.join(root, "public", "logo.png")
theme_path = os.path.join(root, "Sweetkind.json")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme_path)
logo_image = Image.open(logo_path)

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, switch_function):
        super().__init__(master)
        self.grid_columnconfigure(0, weight=1)
        self.switch_function = switch_function
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your username...")
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_submit)
        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Enter your password...")
        
        self.name_entry.pack(pady=(0,10))
        self.password_entry.pack()

        self.login_button.pack(pady=(10,0))
        
    def login_submit(self):
        self.switch_function((self.name_entry.get(), self.password_entry.get()))

class MovieBrowser(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="streaming service", font=FONT)
        self.title_label.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nsew")
        
        self.logo = ctk.CTkImage(logo_image, size=(100,100))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text="", font=FONT)
        self.logo_label.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.title("streaming service")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = LoginScreen(self, switch_function=self.log_in_switch)
        self.login_frame.pack()

        self.browse_frame = MovieBrowser(self)

    def log_in_switch(self, userdata):
        user, password = userdata
        print(f"Logging in as {user} with password {password}")
        self.login_frame.pack_forget()
        self.browse_frame.grid(row=0,column=0,sticky="nsew")

if __name__ == "__main__":
    app = StreamingApp()
    app.mainloop()