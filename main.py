from PIL import Image
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import os

FONT = ("Inter", 14, "bold")

root = Path(__file__).resolve().parent
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(os.path.join(root, "Sweetkind.json"))
logo_image = Image.open(os.path.join(root, "public", "logo.png"))

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
        self.grid_columnconfigure(0, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="STreaming servicentawotihawegaw45y93468y0i9p", font=FONT)
        self.title_label.pack()
        
        self.logo = ctk.CTkImage(logo_image, size=(100,100))
        
        self.bind("<Configure>", self.resize_image)
            
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text="", font=FONT)
        self.logo_label.pack(pady=(20,0))
        

    def resize_image(self, event):
        new_width = event.width
        new_height = event.height
        if new_width > 0 and new_height > 0:
            self.logo.configure(size=(new_width, new_height))
            self.logo_label.configure(image=self.logo)

class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        FONT = ctk.CTkFont("Inter", 14, "bold")
        

        self.title("streaming service")
        self.geometry("400x220")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.login_frame = LoginScreen(self, switch_function=self.log_in_switch)
        self.login_frame.pack()

        self.browse_frame = MovieBrowser(self)

    def log_in_switch(self, userdata):
        user, password = userdata
        print(f"Logging in as {user} with password {password}")
        self.login_frame.pack_forget()
        self.browse_frame.pack()

    def button_callback(self):
        print("hi")


app = StreamingApp()
app.mainloop()
