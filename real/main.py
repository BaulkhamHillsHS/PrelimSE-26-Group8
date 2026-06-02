import time
import random
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import os

TITLE_FONT = ("Inter", 35, "bold")

root = Path(__file__).resolve().parent
resource_path = os.path.join(root, "resource")

logo_path = os.path.join(resource_path, "logo.png")
theme_path = os.path.join(resource_path, "Sweetkind.json")
background_path = os.path.join(resource_path, "placeholder_background.png")
login_background_path = os.path.join(resource_path, "placeholder_background.png")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme_path)
logo_image = Image.open(logo_path)
background_image = Image.open(background_path)
login_background_image = Image.open(login_background_path)

class LoadingScreen(ctk.CTkFrame):
    def __init__(self, master, loading_text):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.loading_bar = ctk.CTkProgressBar(self)
        self.loading_text = ctk.CTkLabel(self, text=loading_text, font=TITLE_FONT)

        self.loading_text.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.loading_bar.grid(row=3, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.loading_bar.configure(mode="indeterminate")
        self.loading_bar.start()

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, switch_function):
        super().__init__(master)
        self.grid_columnconfigure((1), weight=1)
        self.switch_function = switch_function
        self.title_label = ctk.CTkLabel(self, text="henry + benjamin streaming service", font=TITLE_FONT)
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your username...", width=300)
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_submit, hover_color="#3e8a7e", font=TITLE_FONT)
        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Enter your password...", width=300)
        self.stay_logged_in = ctk.CTkSwitch(self, text="Stay logged in")
        #self.login_background = ctk.CTkImage(login_background_image, login_background_image, (1280, 720))
        #self.login_background_label = ctk.CTkLabel(self, image=self.login_background, text="", bg_color="transparent")
        
        self.title_label.grid(row=0, column=1, pady=(50,0))
        self.name_entry.grid(row=1, column=1, pady=(25,10))
        self.password_entry.grid(row=2, column=1, pady=(0,10))
        self.stay_logged_in.grid(row=3, column=1, pady=(10, 0))
        self.login_button.grid(row=4, column=1, pady=(10,0))
        
    def login_submit(self):
        self.switch_function((self.name_entry.get(), self.password_entry.get()))

class MovieBrowser(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(1, weight=1)
        
        self.title_label = ctk.CTkLabel(self, text="streaming service", font=TITLE_FONT)
        self.title_label.grid(row=0, column=1, rowspan=1, columnspan=1, sticky="nsew")
        
        self.logo = ctk.CTkImage(logo_image, size=(100,100))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        self.logo_label.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("streaming service")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        #self.background_image = ctk.CTkImage(background_image, size=(1280,720))
        #self.background_label = ctk.CTkLabel(self, image=self.background_image, text="")

        self.login_frame = LoginScreen(self, switch_function=self.log_in_switch)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.loading_frame = LoadingScreen(self, loading_text="Loading...")
        self.browse_frame = MovieBrowser(self)

    def switch_frame(self, frame1: ctk.CTkFrame, frame2: ctk.CTkFrame):
        frame1.grid_forget()
        frame2.grid(row=0, column=0, sticky="nsew")

    def log_in_switch(self, userdata):
        user, password = userdata
        print(f"Logging in as {user} with password {password}")
        self.switch_frame(self.login_frame, self.loading_frame)
        self.after(3000, lambda:self.switch_frame(self.loading_frame, self.browse_frame))

if __name__ == "__main__":
    app = StreamingApp()
    app.mainloop()