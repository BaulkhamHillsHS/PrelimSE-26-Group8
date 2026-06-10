import time
import random
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
import os

TITLE_FONT = ("Inter", 35, "bold")
TEXT_FONT = ("Arial", 20)
IDK_FONT = ("Courier New", 14)

root = Path(__file__).resolve().parent
resource_path = os.path.join(root, "resource")

image_names = [
          "settings_icon",
          "home_icon",
          "search_icon",
          "star_icon",
          "quit_icon",
          "account_icon",
          "logo",
          ]

images = {}

for name in image_names:
    image_path = os.path.join(resource_path, name+".png")
    image = Image.open(image_path)
    images[name] = image

theme_path = os.path.join(resource_path, "Sweetkind.json")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme_path)

class LoadingScreen(ctk.CTkFrame):
    def __init__(self, master, loading_text: str):
        super().__init__(master)
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 5), weight=1)
        self.loading_text = loading_text
        self.build_ui()

    def build_ui(self):
        self.loading_bar = ctk.CTkProgressBar(self)
        self.loading_label = ctk.CTkLabel(self, text=self.loading_text, font=TITLE_FONT)
        self.loading_label.grid(row=2, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.loading_bar.grid(row=3, column=1, padx=(10, 10), pady=(10, 10), sticky="ew")
        self.loading_bar.configure(mode="indeterminate")
        self.loading_bar.start()

class LoginScreen(ctk.CTkFrame):
    def __init__(self, master, switch_function):
        super().__init__(master)
        self.grid_columnconfigure((1), weight=1)
        self.switch_function = switch_function
        self.show_password_state = tk.BooleanVar(value=False)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="HBflix login", font=TITLE_FONT)
        self.name_entry = ctk.CTkEntry(self, placeholder_text="Enter your username...", width=300)
        self.login_button = ctk.CTkButton(self, text="Login", command=self.login_submit, hover_color="#3e8a7e", font=TITLE_FONT)
        self.password_entry = ctk.CTkEntry(self, show="*", placeholder_text="Enter your password...", width=300)
        self.show_password = ctk.CTkCheckBox(self, text="Show password", variable=self.show_password_state, command=self.toggle_show_password)
        #self.login_background = ctk.CTkImage(login_background_image, login_background_image, (1280, 720))
        #self.login_background_label = ctk.CTkLabel(self, image=self.login_background, text="", bg_color="transparent")
        self.title_label.grid(row=0, column=1, pady=(50,30))
        self.name_entry.grid(row=1, column=1, pady=(25,10))
        self.password_entry.grid(row=2, column=1, pady=(0,10))
        self.show_password.grid(row=3, column=1, pady=(20, 20))
        self.login_button.grid(row=4, column=1, pady=(10,0))
        
    def login_submit(self):
        if self.name_entry.get() == "":
            self.switch_function(("Guest", ""))
        else:
            self.switch_function((self.name_entry.get(), self.password_entry.get()))

    def toggle_show_password(self):
        if self.show_password_state.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

class Sidebar(ctk.CTkFrame):
    def __init__(self, master, handle_function):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(5, minsize=60)
        self.grid_rowconfigure((0, 1, 2, 3, 4, 6), weight=1)
        self.handle_function = handle_function
        self.build_ui()

    def build_ui(self):
        self.home_image = ctk.CTkImage(images["home_icon"], size=(48, 48))
        self.home_button = ctk.CTkButton(self, image=self.home_image, text="", command=lambda: self.handle_button_press("home"))

        self.settings_image = ctk.CTkImage(images["settings_icon"], size=(48, 48))
        self.settings_button = ctk.CTkButton(self, image=self.settings_image, text="", command=lambda: self.handle_button_press("settings"))

        self.search_image = ctk.CTkImage(images["search_icon"], size=(48, 48))
        self.search_button = ctk.CTkButton(self, image=self.search_image, text="", command=lambda: self.handle_button_press("search"))

        self.star_image = ctk.CTkImage(images["star_icon"], size=(48, 48))
        self.star_button = ctk.CTkButton(self, image=self.star_image, text="", command=lambda: self.handle_button_press("star"))

        self.quit_image = ctk.CTkImage(images["quit_icon"], size=(48, 48))
        self.quit_button = ctk.CTkButton(self, image=self.quit_image, text="", command=lambda: self.handle_button_press("quit"))

        self.account_image = ctk.CTkImage(images["account_icon"], size=(48, 48))
        self.account_button = ctk.CTkButton(self, image=self.account_image, text="", command=lambda: self.handle_button_press("account"))

        self.home_button.grid(row=0, column=0, pady=(10, 10), sticky="nsew")
        self.search_button.grid(row=1, column=0, pady=(10, 10), sticky="nsew")
        self.star_button.grid(row=2, column=0, pady=(10, 10), sticky="nsew")
        self.settings_button.grid(row=3, column=0, pady=(10, 10), sticky="nsew")
        self.quit_button.grid(row=4, column=0, pady=(10, 10), sticky="nsew")
        self.account_button.grid(row=6, column=0, pady=(10, 10), sticky="nsew")

    def handle_button_press(self, button):
        self.handle_function(button)

class Moviebar(ctk.CTkScrollableFrame):
    def __init__(self, master, movies):
        super().__init__(master, orientation="horizontal")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.movies = movies
        self.movie_images = []
        self.build_ui()

    def build_ui(self):
        for i, movie in enumerate(self.movies):
            movie_image = ctk.CTkImage(images["logo"], size=(64, 128))
            movie_label = ctk.CTkLabel(self, image=movie_image, text="", fg_color="transparent")
            self.movie_images.append(movie_image)
            movie_label.grid(row=0, column=i, sticky="ew", pady=0, padx=(10, 10))

class LabelledMoviebar(ctk.CTkFrame):
    def __init__(self, master, name, movies):
        super().__init__(master)
        self.name = name
        self.movies = movies
        self.movie_bar = Moviebar(self, self.movies)
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure(0, weight=1)
        self.build_ui()

    def build_ui(self):
        self.label = ctk.CTkLabel(self, text=self.name, font=TEXT_FONT)
        self.label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.movie_bar.grid(row=1, column=0, sticky="ew", pady=0)

class HomeFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, name):
        super().__init__(master, fg_color="transparent")
        self.name = name

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)
        self.movie_bar_1 = LabelledMoviebar(self, name="Recommended movies", movies=[0]*20)
        self.movie_bar_2 = LabelledMoviebar(self, name="TV shows", movies=[0]*3)
        self.movie_bar_3 = LabelledMoviebar(self, name="placeholder 3", movies=[0])

        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text=f"Welcome, {self.name}", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew")
        self.movie_bar_1.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.movie_bar_2.grid(row=2, column=0, sticky="nsew")
        self.movie_bar_3.grid(row=3, column=0, sticky="nsew")

    def change_name(self, new_name):
        self.name = new_name
        self.title_label.configure(text=f"Welcome, {self.name}")

class FilterSortFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.restrictions_map = {
            "any": [""],
            "score rating": [">9", ">8.5", ">8", ">7"],
            "age rating": ["PG", "PG13", "MA15+", "M", "R"],
            "length": ["<75m", "<90m", "<120m", ">75m", ">90m", ">120m"],
            "genre": ["sci-fi", "action", "fantasy", "whatever"]
        }

        self.build_ui()

    def build_ui(self):
        self.filter_by = ctk.CTkOptionMenu(self, values=["any", "score rating", "age rating", "length", "genre"], command=self.filter_change)
        self.filter_by_restriction_menu = ctk.CTkOptionMenu(self, values=self.restrictions_map["any"])
        self.sort_by = ctk.CTkOptionMenu(self, values=["score rating", "age rating", "length", "genre"])

        self.filter_label = ctk.CTkLabel(self, text="Filter by...", font=TEXT_FONT)
        self.sort_label = ctk.CTkLabel(self, text="Sort by...", font=TEXT_FONT)

        self.filter_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        self.sort_label.grid(row=0, column=2, padx=10, pady=10)

        self.filter_by.grid(row=1, column=0, padx=10, pady=10)
        self.filter_by_restriction_menu.grid(row=1, column=1, padx=10, pady=10)
        self.sort_by.grid(row=1, column=2, padx=10, pady=10)

    def filter_change(self, new: str):
        if new in self.restrictions_map:
            self.filter_by_restriction_menu.configure(values=self.restrictions_map[new])
            self.filter_by_restriction_menu.set(self.restrictions_map[new][0])

    def get_filter(self):
        return (self.filter_by.get(), self.filter_by_restriction_menu.get())
    
    def get_sort(self):
        return (self.sort_by.get())

class SearchFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Search", font=TITLE_FONT)
        self.filter_sort_frame = FilterSortFrame(self)
        self.a_button = ctk.CTkButton(self, text="Search button", command=self.button_callback)

        self.title_label.grid(row=0, column=0, sticky="nsew")
        self.filter_sort_frame.grid(row=1, column=0)
        self.a_button.grid(row=2, column=0)
        
    def button_callback(self):
        print(self.filter_sort_frame.get_filter())
        print(self.filter_sort_frame.get_sort())

class StarredFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Starred movies and TV shows", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew")

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Settings", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew")

class AccountFrame(ctk.CTkFrame):
    def __init__(self, master, name):
        super().__init__(master, fg_color="transparent")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.name = name
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Account", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew")

    def change_name(self, new_name):
        self.name = new_name
        self.title_label.configure(text=f"Account: {self.name}")

class MovieBrowser(ctk.CTkFrame):
    def __init__(self, master, name, quit):
        super().__init__(master)
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)

        self.quit = quit
        self.name = name
        self.home_frame = HomeFrame(self, self.name)
        self.search_frame = SearchFrame(self)
        self.star_frame = StarredFrame(self)
        self.settings_frame = SettingsFrame(self)
        self.account_frame = AccountFrame(self, self.name)

        self.current_frame = self.home_frame

        self.build_ui()
    
    def build_ui(self):
        self.logo = ctk.CTkImage(images["logo"], size=(100,100))
        self.logo_label = ctk.CTkLabel(self, image=self.logo, text="")
        self.logo_label.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

        self.sidebar = Sidebar(self, self.handle_sidebar)
        self.sidebar.grid(row=1, column=0, pady=(50, 10), padx=(10, 10), sticky="ns")

        self.home_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", pady=(10, 10), padx=(10, 10))

    def handle_sidebar(self, button_name):
        if button_name == "quit":
            self.quit()
        else:
            match button_name:
                case "home":
                    self.switch_frame(self.home_frame)
                case "star":
                    self.switch_frame(self.star_frame)
                case "settings":
                    self.switch_frame(self.settings_frame)
                case "search":
                    self.switch_frame(self.search_frame)
                case "account":
                    self.switch_frame(self.account_frame)

    def change_name(self, new_name: str):
        self.home_frame.change_name(new_name)
        self.account_frame.change_name(new_name)

    def switch_frame(self, new_frame):
        self.current_frame.grid_forget()
        new_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", pady=(10, 10), padx=(10, 10))
        self.current_frame = new_frame

class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("streaming service")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.user = ""
        self.build_ui()

    def build_ui(self):
        #self.background_image = ctk.CTkImage(background_image, size=(1280,720))
        #self.background_label = ctk.CTkLabel(self, image=self.background_image, text="")

        self.login_frame = LoginScreen(self, switch_function=self.log_in_switch)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.loading_frame = LoadingScreen(self, loading_text="Loading...")
        self.browse_frame = MovieBrowser(self, self.user, quit=self.quit)

    def switch_frame(self, frame1: ctk.CTkFrame, frame2: ctk.CTkFrame):
        frame1.grid_forget()
        frame2.grid(row=0, column=0, sticky="nsew")

    def log_in_switch(self, userdata):
        user, password = userdata
        print(f"Logging in as {user} with password {password}")
        self.switch_frame(self.login_frame, self.loading_frame)
        self.user = user
        self.browse_frame.change_name(user)
        self.after(500, lambda:self.switch_frame(self.loading_frame, self.browse_frame))

    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = StreamingApp()
    app.mainloop()