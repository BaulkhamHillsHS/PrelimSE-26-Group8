from typing import Union
import json
import csv
import time
import random
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from enum import Enum
import os

TITLE_FONT = ("Inter", 35, "bold")
TEXT_FONT = ("Arial", 20)
IDK_FONT = ("Courier New", 14)
POSTER_SIZE = (96, 144)
FILTER_SORT_OPTIONS = ["any", "score rating", "age rating", "length", "genre", "popularity"]
RESTRICTIONS_MAP = {
            "any": [""],
            "score rating": [">9", ">8.5", ">8", ">7"],
            "age rating": ["PG", "PG13", "MA15+", "M", "R"],
            "length": ["<75m", "<90m", "<120m", ">75m", ">90m", ">120m"],
            "genre": ["Science Fiction", "Action", "Fantasy", "Comedy", "Adventure"],
            "popularity": [">200", ">175", ">150", ">100", ">50"]
        }

root = Path(__file__).resolve().parent
resource_path = os.path.join(root, "resource")
posters_path = os.path.join(resource_path, "posters")

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

def read_json(filepath: str):
    assert os.path.exists(filepath)
    with open(filepath, "r") as f:
        data = json.load(f)
    return data

def write_json(obj, filepath: str):
    assert os.path.exists(filepath)
    with open(filepath, "w") as f:
        json.dump(obj, f)

json_names = [
    "movie",
    "tv",
    "anime_movie",
    "anime",
]

jsons = {}

for name in json_names:
    json_path = os.path.join(resource_path, name+".json")
    data = read_json(json_path)
    jsons[name] = data

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(os.path.join(resource_path, "theme.json"))

def movie_get_attribute(movie_data, attribute) -> Union[str, int, float]:
    match attribute:
        case "score_rating":
            return movie_data["vote_average"]
        case "age rating":
            raise ValueError() # FIXME:
        case "length":
            return movie_data["runtime"]
        case "genre":
            return movie_data["genres"]
        case "popularity":
            return movie_data["popularity"]
    raise ValueError() # FIXME:

def restriction_check(filter: str, restriction: str, movie_data: dict):
    assert filter in FILTER_SORT_OPTIONS
    assert restriction in RESTRICTIONS_MAP[filter]
    match filter:
        case "any":
            return True
        case "score rating":
            movie_score = movie_data["vote_average"] #FIXME: why hardcode movie? also, use the movie_get_attribute function or similar
            required = float(restriction[1:])
            return movie_score>=required
        case "age rating":
            raise ValueError() # No age ratings yet... FIXME:
        case "length":
            movie_length = movie_data["runtime"]
            required = int(restriction[1:-1])
            if restriction[0]=="<":
                return movie_length<required
            else:
                return movie_length>required
        case "genre":
            movie_genres = movie_data["genres"]
            for genre in movie_genres:
                if genre["name"]==restriction:
                    return True
            return False
        case "popularity":
            movie_popularity = movie_data["popularity"]
            required = int(restriction[1:])
            return movie_popularity>=required
    raise ValueError()  # FIXME: debug, delete later
    return False

def get_media(media_type: str, filter_by: str, restriction: str, sort_by: str, count: int):
    match media_type:
        case "movie":
            media_dict = jsons["movie"]
        case "tv_show":
            media_dict = jsons["tv"]
        case "anime_movie":
            media_dict = jsons["anime_movie"]
        case "anime":
            media_dict = jsons["anime"]
        case _:
            raise ValueError()
        
    assert filter_by, sort_by in FILTER_SORT_OPTIONS
    assert restriction in RESTRICTIONS_MAP[filter_by]
    out = []
    for movie in media_dict:
        if restriction_check(filter_by, restriction, movie):
            out.append(movie)
    if sort_by=="any":
        return out[:count]
    out.sort(key=lambda x: movie_get_attribute(x, sort_by)) # FIXME: tv show anime support
    return out[:count]

print(*get_media("movie", "score rating", ">8.5", "any", 10))
# FIXME: debug command

class SubscriptionPlan(Enum):
    BRONZE = "Bronze"
    SILVER = "Silver"
    GOLD = "Gold"
    PLATINUM = "Platinum"

class Profile:
    def __init__(self, name, age_rating):
        self.name = name
        self.age_rating = age_rating
        self.watchlist = []
        self.watch_history = []

class Account:
    def __init__(self, name, email, password, subscription_plan: SubscriptionPlan, payment_info):
        self.name = name
        self.email = email
        self.__password = password
        self.__payment_info = payment_info
        self.subscription_plan = subscription_plan
        self.profiles = []

    def check_password(self, attempt):
        return attempt==self.__password
    
    def get_password(self):
        return self.__password
    
    def get_payment_info(self):
        return self.__payment_info
    
class AccountManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.fields = ["name", "email", "password", "subscription_plan", "payment_info", "profiles"]
    
    def load_accounts(self):
        accounts = []
        with open(self.filepath, "r", newline="") as f:
            reader=csv.DictReader(f)
            for row in reader:
                accounts.append(Account(row["name"], row["email"], row["password"], SubscriptionPlan(row["subscription_plan"]), row["payment_info"]))
        return accounts
    
    def save_account(self, account: Account):
        with open(self.filepath, "a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writerow({
                "name": account.name, 
                "email": account.email, 
                "password": account.get_password(), 
                "subscription_plan": account.subscription_plan.value, 
                "payment_info": account.get_payment_info(),
                "profiles": str(account.profiles)
                })

class Media():
    def __init__(self, media_data: dict, dimensions: tuple[int, int]):
        self.media_data = media_data
        self.dimensions=dimensions
        self.set_poster()

    def set_poster(self):
        self.pillow_image = Image.open(os.path.join(posters_path, f"m_{self.get_id()}"))
        self.poster = ctk.CTkImage(self.pillow_image, size=self.dimensions) # FIXME: # type: ignore

    def change_image_size(self, width, height):
        self.poster.configure(size=(width, height))

    def get_poster(self):
        return self.poster
    
    def get_data(self, key=None):
        if key in self.media_data:
            return self.media_data[key]
        return self.media_data
    
    def get_runtime(self):
        return self.get_data("runtime")
    
    def __str__(self) -> str:
        return "Base Media"
    
    def get_title(self) -> str:
        return str(self.get_data("title"))

    def get_id(self) -> int:
        movie_id = self.get_data("id")
        assert type(movie_id) == int
        return movie_id
    
class Movie(Media):
    def __init__(self, media_data: dict, dimensions: tuple[int, int]=(500, 750)):
        super().__init__(media_data, dimensions)
    
    def set_poster(self):
        self.pillow_image = Image.open(os.path.join(posters_path, f"m_{self.get_id()}.jpg"))
        self.poster = ctk.CTkImage(self.pillow_image, size=self.dimensions)

    def __str__(self) -> str:
        return str(self.get_title())

class Show(Media):
    def __init__(self, media_data, dimensions: tuple[int, int]=(500, 750)):
        super().__init__(media_data, dimensions=dimensions)
        season_data = self.get_data("seasons")
        self.season_count = len(season_data)
        self.seasons = [Season(season_data[i]) for i in range(self.season_count)]

    def __str__(self) -> str:
        return str(self.get_data("name"))
    
    def get_seasons(self):
        return self.seasons
    
    def get_season_n(self, n):
        if not(0<=n<self.season_count):
            return {}
        return self.get_seasons()[n]
    
    def set_poster(self):
        self.pillow_image = Image.open(os.path.join(posters_path, f"tv_{self.get_id()}"))
        self.poster = ctk.CTkImage(self.pillow_image, size=self.dimensions)

class Season():
    def __init__(self, media_data: dict, dimensions=(500, 750)):
        self.media_data = media_data
        self.season_number = self.get_data("season_number")
        self.pillow_image = Image.open(os.path.join(posters_path, f"s_{self.get_id()}")) # FIXME: incomplete imp
        self.poster = ctk.CTkImage(self.pillow_image, size=dimensions)
    
    def get_data(self, key=None):
        if key in self.media_data:
            return self.media_data[key]
        return self.media_data

    def get_episode_count(self):
        return str(self.get_data("episode_count"))

    def __str__(self) -> str:
        return str(self.get_data("name"))

    def get_id(self) -> int:
        movie_id = self.get_data("id")
        assert type(movie_id) == int
        return movie_id
    
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
            assert type(movie)==Movie
            movie_image = movie.get_poster()
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
        self.movie_bar_1 = LabelledMoviebar(self, name="Recommended movies", movies=[Movie(random.choice(jsons["movie"]), POSTER_SIZE) for x in range(20)])
        self.movie_bar_2 = LabelledMoviebar(self, name="TV shows", movies=[Movie(random.choice(jsons["movie"]), POSTER_SIZE) for x in range(5)])
        self.movie_bar_3 = LabelledMoviebar(self, name="placeholder 3", movies=[])
        self.movie_bar_4 = LabelledMoviebar(self, name="Explore(random)", movies=[Movie(random.choice(jsons["movie"]), POSTER_SIZE) for x in range(5)]) # FIXME: Hack
        self.movie_bar_5 = LabelledMoviebar(self, name="Explore(not random)", movies=[Movie(jsons["movie"][i], POSTER_SIZE) for i in range(5)]) # FIXME: Hack

        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text=f"Welcome, {self.name}", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew")
        self.movie_bar_1.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.movie_bar_2.grid(row=2, column=0, sticky="nsew")
        self.movie_bar_3.grid(row=3, column=0, sticky="nsew")
        self.movie_bar_4.grid(row=4, column=0, sticky="nsew")
        self.movie_bar_5.grid(row=5, column=0, sticky="nsew")

    def change_name(self, new_name):
        self.name = new_name
        self.title_label.configure(text=f"Welcome, {self.name}")

class FilterSortFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.columnconfigure((0, 1, 2), weight=1)
        self.rowconfigure((0, 1), weight=1)
        self.restrictions_map = RESTRICTIONS_MAP

        self.build_ui()

    def build_ui(self):
        self.filter_by = ctk.CTkOptionMenu(self, values=FILTER_SORT_OPTIONS, command=self.filter_change)
        self.filter_by_restriction_menu = ctk.CTkOptionMenu(self, values=self.restrictions_map["any"])
        self.sort_by = ctk.CTkOptionMenu(self, values=FILTER_SORT_OPTIONS)

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
        self.rowconfigure((0, 1), weight=1)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Settings", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew")

        self.tabs= ctk.CTkTabview(self)
        self.tabs.add("Settings1")
        self.tabs.add("Settings2")
        self.tabs.grid(row=1, column=0, sticky="nsew")

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