from datetime import datetime
from typing import Union
from PIL import Image
from PIL import ImageTk, ImageEnhance
import json
import csv
import random
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from pathlib import Path
from enum import Enum
import os

TITLE_FONT = ("Inter", 35, "bold")
TEXT_FONT = ("Arial", 20)
SMALL_FONT = ("Arial", 17)
TYPEWRITER_FONT = ("Courier New", 14)

POSTER_SIZE = (96, 144)
MEDIUM_POSTER_SIZE = (160, 240)
BIG_POSTER_SIZE = (320, 480)

FILTER_SORT_OPTIONS = ["any", "score rating", "age rating", "length", "genre", "popularity"]
RESTRICTIONS_MAP = {
            "any": [""],
            "score rating": [">8.5", ">8", ">7.5", ">7"],
            "age rating": ["PG", "PG13", "MA15+", "M", "R"],
            "length": ["<75m", "<90m", "<120m", ">75m", ">90m", ">120m"],
            "genre": ["Science Fiction", "Action", "Fantasy", "Comedy", "Adventure"],
            "popularity": [">200", ">175", ">150", ">100", ">50"]
        }

root = Path(__file__).resolve().parent
resource_path = os.path.join(root, "resource")
posters_path = os.path.join(resource_path, "posters")

image_names = [
          # HENRY STUFF
          "settings_icon",
          "home_icon",
          "search_icon",
          "star_icon",
          "quit_icon",
          "account_icon",
          "logo",
          # BEN STUFF
          "blind",
          "eye",
          "logo_dark",
          "logo_light",
          "lock",
          "person",
          "main_logo"
          ]

images = {}

for name in image_names:
    image_path = os.path.join(resource_path, name+".png")
    image = Image.open(image_path)
    images[name] = image

def pretty_time(minutes: int, clock=False):
    if clock:
        return f"{minutes//60}:{minutes%60}"
    else:
        return f"{minutes//60}h{minutes%60}m"
    
def get_current():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

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

accounts_path = os.path.join(resource_path, "accounts.csv")

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(os.path.join(resource_path, "theme.json"))

class SubscriptionPlan(Enum):
    FREE = "FreePlan"
    STANDARD = "StandardPlan"
    PREMIUM = "PremiumPlan"

class Profile:
    def __init__(self, name, is_adult: bool, watchlist=None, watch_history=None):
        self.name = name
        self.is_adult = is_adult
        self.watchlist = watchlist if watchlist is not None else []
        self.watch_history = watch_history if watch_history is not None else []

    def to_dict(self):
        return {
            "name": self.name,
            "is_adult": self.is_adult,
            "watchlist": self.watchlist,
            "watch_history": self.watch_history
        }
    
class Account:
    def __init__(self, username, email, password, subscription_plan: SubscriptionPlan, payment_info):
        self.username = username
        self.email = email
        self.subscription_plan = subscription_plan

        # ENCAPSULATION
        self.__password = password
        self.__payment_info = payment_info

        # COMPOSITION
        self.profiles = []

    def check_password(self, attempt):
        return attempt==self.__password
    
    def get_password(self):
        return self.__password
    
    def get_payment_info(self):
        return self.__payment_info
    
    def add_profile(self, profile: Profile):
        self.profiles.append(profile)
    
class AccountManager:
    def __init__(self, filepath):
        self.filepath = filepath
        self.fields = ["username", "email", "password", "subscription_plan", "payment_info", "profiles"]
    
    def load_accounts(self):
        accounts = []
        if not os.path.exists(self.filepath):
            return accounts
        
        with open(self.filepath, "r", newline="", encoding="utf-8") as f:
            reader=csv.DictReader(f)
            for row in reader:
                plan_value = row["subscription_plan"].strip()
                plan = ([plan for plan in SubscriptionPlan if plan.value == plan_value]+[SubscriptionPlan.FREE])[0]
                account = Account(row["username"], row["email"], row["password"], plan, row["payment_info"])
                profiles = json.loads(row["profiles"])
                for profile_data in profiles:
                    profile = Profile(profile_data["name"], profile_data["is_adult"], profile_data.get("watchlist", []), profile_data.get("watch_history", []))
                    account.add_profile(profile)

                accounts.append(account)

        return accounts
    
    def save_account(self, account: Account):
        file_exists = os.path.exists(self.filepath)
        with open(self.filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "username": account.username, 
                "email": account.email, 
                "password": account.get_password(), 
                "subscription_plan": account.subscription_plan.value, 
                "payment_info": account.get_payment_info(),
                "profiles": json.dumps([p.to_dict() for p in account.profiles])
                })
            
    def update_accounts(self, accounts: list[Account]):
        with open(self.filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=self.fields)
            writer.writeheader()
            for account in accounts:
                writer.writerow({
                    "username": account.username, 
                    "email": account.email, 
                    "password": account.get_password(), 
                    "subscription_plan": account.subscription_plan.value, 
                    "payment_info": account.get_payment_info(),
                    "profiles": json.dumps([p.to_dict() for p in account.profiles])
                })

class Media():
    def __init__(self, media_data: dict, dimensions: tuple[int, int]):
        self.media_data = media_data
        self.set_poster(dimensions)

    def set_poster(self, dimensions):
        self.pillow_image = Image.open(os.path.join(posters_path, f"m_{self.get_id()}.jpg"))
        self.poster = ctk.CTkImage(self.pillow_image, size=dimensions)

    def get_overview(self):
        return self.get_data("overview", "")

    def get_poster(self, size=None):
        if size:
            return ctk.CTkImage(self.pillow_image, size=size)
        return self.poster
    
    def get_data(self, key: str, default):
        return self.media_data.get(key, default)
    
    def get_runtime(self):
        return self.get_data("runtime", 0)
    
    def __str__(self) -> str:
        return "Base Media"
    
    def get_title(self) -> str:
        return str(self.get_data("title", ""))

    def get_id(self) -> int:
        movie_id = self.get_data("id", 0)
        assert type(movie_id) == int
        return movie_id
    
class Movie(Media):
    def __init__(self, media_data: dict, dimensions: tuple[int, int]=POSTER_SIZE):
        super().__init__(media_data, dimensions)

    def __str__(self) -> str:
        return f"{self.get_title()}({self.get_runtime()})"

class Anime(Media):
    def __init__(self, media_data, dimensions: tuple[int, int]=POSTER_SIZE):
        super().__init__(media_data, dimensions=dimensions)
        season_data = self.get_data("seasons", [])
        self.season_count = len(season_data)
        self.seasons = [Season(season_data[i]) for i in range(self.season_count)]

    def __str__(self) -> str:
        return str(self.get_data("name", ""))
    
    def get_seasons(self):
        return self.seasons
    
    def get_season_n(self, n):
        if not(0<=n<self.season_count):
            return {}
        return self.get_seasons()[n]
    
    def set_poster(self, dimensions):
        self.pillow_image = Image.open(os.path.join(posters_path, f"t_{self.get_id()}.jpg"))
        self.poster = ctk.CTkImage(self.pillow_image, size=dimensions)

    def get_title(self):
        return self.get_data("name", "")

class AnimeMovie(Media):
    def __init__(self, media_data: dict, dimensions: tuple[int, int]=(500, 750)):
        super().__init__(media_data, dimensions)

    def __str__(self) -> str:
        return f"{self.get_title()}({self.get_runtime()})"

class Show(Media):
    def __init__(self, media_data, dimensions: tuple[int, int]=POSTER_SIZE):
        super().__init__(media_data, dimensions=dimensions)
        season_data = self.get_data("seasons", [])
        self.season_count = len(season_data)
        self.seasons = [Season(season_data[i]) for i in range(self.season_count)]

    def __str__(self) -> str:
        return str(self.get_data("name", ""))
    
    def get_seasons(self):
        return self.seasons
    
    def get_season_n(self, n):
        if not(0<=n<self.season_count):
            return {}
        return self.get_seasons()[n]
    
    def set_poster(self, dimensions):
        self.pillow_image = Image.open(os.path.join(posters_path, f"t_{self.get_id()}.jpg"))
        self.poster = ctk.CTkImage(self.pillow_image, size=dimensions)

    def get_title(self):
        return self.get_data("name", "")

class Episode():
    def __init__(self, episode_number: int):
        self.episode_number = episode_number
    
    def __str__(self) -> str:
        return str(self.episode_number)

class Season():
    def __init__(self, media_data: dict, dimensions=POSTER_SIZE):
        self.media_data = media_data
        self.season_number = self.get_data("season_number", 0)
        self.dimensions = dimensions
        #self.pillow_image = Image.open(os.path.join(posters_path, f"s_{self.get_id()}.jpg")) # FIXME: incomplete imp
        #self.poster = ctk.CTkImage(self.pillow_image, size=dimensions)
        self.episode_count = int(self.get_data("episode_count", 0)) # 
        #self.episodes = [Episode(i) for i in range(1, self.episode_count+1)] FIXME: lag
    
    def get_data(self, key: str, default):
        return self.media_data.get(key, default)

    def get_episode_count(self):
        return str(self.episode_count)

    def __str__(self) -> str:
        return str(self.get_data("name", ""))

    def get_id(self) -> int:
        movie_id = self.get_data("id", 0)
        assert type(movie_id) == int
        return movie_id
    
def media_get_attribute(data, attribute, default) -> Union[str, int, float]:
    match attribute:
        case "score_rating":
            return data["vote_average"]
        case "age rating":
            raise ValueError() # FIXME:
        case "length":
            return data["runtime"]
        case "genre":
            return data["genres"]
        case "popularity":
            return data["popularity"]
        case _:
            return data.get(attribute, default)

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

def get_media(media_type: str, filter_by: str, restriction: str, sort_by: str, count: int, decreasing: bool=False):
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

    if sort_by!="any":
        out.sort(key=lambda x: media_get_attribute(x, sort_by, 0), reverse=decreasing)

    match media_type:
        case "movie":
            return [Movie(x) for x in out[:count]]
        case "tv_show":
            return [Show(x) for x in out[:count]]
        case "anime_movie":
            return [AnimeMovie(x) for x in out[:count]]
        case "anime":
            return [Anime(x) for x in out[:count]]

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

def create_rrect(canvas: ctk.CTkCanvas, width, height, pos, r, fill):
    x1, y1 = pos
    x2 = x1 + width
    y2 = y1 + height
    points = [
        # corner 1
        x1, y1 + r, x1, y1 + r,
        x1, y1,
        x1 + r, y1, x1 + r, y1,
        
        # corner 2
        x2 - r, y1, x2 - r, y1,
        x2, y1,
        x2, y1 + r, x2, y1 + r,
        
        # corner 3
        x2, y2 - r, x2, y2 - r,
        x2, y2,
        x2 - r, y2, x2 - r, y2,
        
        # corner 4
        x1 + r, y2, x1 + r, y2,
        x1, y2,
        x1, y2 - r, x1, y2 - r
    ]
    return canvas.create_polygon(points, smooth=True, fill=fill)

class ImageCell():
    def __init__(self, canvas: ctk.CTkCanvas, image, pos, speed = 1.0):
        self.canvas = canvas
        self.id = self.canvas.create_image(*pos, image=image, anchor="nw")
        self.speed = speed
    
    def move(self, x, y):
        self.canvas.move(self.id, x, y)
    
    def goto(self, x, y):
        self.canvas.moveto(self.id, x, y)
    
    def slide(self):
        self.canvas.move(self.id, self.speed, 0)
    
    def get_pos(self):
        return self.canvas.tk.call(self.canvas._w, "coords", self.id) # FIXME: # type: ignore
    
    def get_size(self):
        bbox = self.canvas.bbox(self.id)
        x = bbox[2] - bbox[0]
        y = bbox[3] - bbox[1]
        return (x, y)
    
class Panel():
    def __init__(self, canvas: ctk.CTkCanvas, width, height, r, pos, fill, padding):
        self.canvas = canvas
        self.width = width
        self.height = height
        self.pos = pos
        self.padding = padding
        create_rrect(canvas, width, height, pos, r, fill)
    
    def get_pos(self):
        return (self.pos[0] - 2, self.pos[1])
    
    def get_dim(self):
        return (self.width, self.height)
    
    def get_udim(self):
        return (self.width - self.padding[0] - self.padding[1], self.height - self.padding[2] - self.padding[3])

class LoginFrame(ctk.CTkFrame):
    def __init__(
        self,
        master,
        login_switch
    ):
        super().__init__(master=master, width=1280, height=720, fg_color="transparent")
        self.width = 1280
        self.height = 720 
        self.login_switch = login_switch

        self.update()
        self.build_ui()
        
    def build_ui(self):
        self.images_count = 9
        self.row_count = 7
        
        pil_image = images["logo_light"]
        pil_image_dark = ImageEnhance.Brightness(images["logo_light"]).enhance(0.6)

        main_font = ctk.CTkFont(family="Inter Regular", size=16)

        self.image_sizes = [(90, 90), (60, 60)]
        self.image = ImageTk.PhotoImage(pil_image.resize(self.image_sizes[0]))
        self.image_dark = ImageTk.PhotoImage(pil_image_dark.resize(self.image_sizes[1]))
        
        self.canvas = ctk.CTkCanvas(self, width=1280, height=720, bg="black", highlightthickness=0)
        self.canvas.place(x=0, y=0)

        self.images = []
        for j in range(self.row_count):
            y_pos = self.height / (self.row_count - 1) * j - self.image_sizes[j % 2][0] / 2
            x_offset = (j // 2) % 2 * self.width / self.images_count / 2
            # speed = random.randint(40, 100) / 50
            speed = (1 + j % 2) / 3
            for i in range(self.images_count + 1):
                image = ImageCell(self.canvas, self.image if j % 2 == 0 else self.image_dark, (self.width / self.images_count * i - self.image_sizes[j % 2][0] / 2 + x_offset, y_pos), speed)
                self.images.append(image)
        
        login_panel = Panel(self.canvas, (w:=400), (f := 0.85)*self.height, 40, ((self.width - w) / 2, (1 - f)*self.height / 2), "#36363B", (30, 30, 30, 30))
        
        title = images["main_logo"]
        title_pad = 30
        
        self.asdf = ImageTk.PhotoImage(title.resize(((w_x:=login_panel.get_udim()[0] - 2 * title_pad), int(title.size[1] / title.size[0] * w_x))))
        self.netflix = self.canvas.create_image(login_panel.pos[0] + login_panel.padding[0] + title_pad, login_panel.pos[1] + login_panel.padding[2] + title_pad, image=self.asdf, anchor="nw")
        
        self.email_frame = ctk.CTkFrame(self, login_panel.get_udim()[0], 56, 10, bg_color="#36363B", fg_color="#4C4C53", border_width=2, border_color="#6F6F70")
        self.email_frame.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=self.canvas.bbox(self.netflix)[3] + 40)
        self.email_frame.rowconfigure(0, weight=1)
        self.email_frame.columnconfigure(1, weight=1)
        self.email_frame.grid_propagate(False)
        
        self.email = ctk.CTkEntry(self.email_frame, font=main_font, placeholder_text="Email or mobile number", border_width=0, fg_color="#4C4C53", text_color="#98989B")
        self.email.grid(row=0, column=1, sticky="nesw", pady=2, padx=(0, 15))
        self.person_icon = ctk.CTkLabel(self.email_frame, image=ctk.CTkImage(light_image=(p:=images["person"]), size=p.size), text="")
        self.person_icon.grid(row=0, column=0, padx=(12, 10))
        
        self.password_frame = ctk.CTkFrame(self, login_panel.get_udim()[0], 56, 10, bg_color="#36363B", fg_color="#4C4C53", border_width=2, border_color="#6F6F70")
        self.password_frame.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=self.canvas.bbox(self.netflix)[3] + 40 + 56 + 24)
        self.password_frame.rowconfigure(0, weight=1)
        self.password_frame.columnconfigure(1, weight=1)
        self.password_frame.grid_propagate(False)
        
        self.password = ctk.CTkEntry(self.password_frame, font=main_font, placeholder_text="Password", border_width=0, fg_color="#4C4C53", show="•", text_color="#98989B")
        self.password.grid(row=0, column=1, sticky="nesw", pady=2, padx=(0, 15))
        self.lock_icon = ctk.CTkLabel(self.password_frame, image=ctk.CTkImage(light_image=(p:=images["lock"]), size=p.size), text="")
        self.lock_icon.grid(row=0, column=0, padx=(12, 10))
        
        self.visibility = [images["eye"], images["blind"]]
        self.hide = ctk.CTkButton(self.password_frame, width=0, height=40, text="", fg_color="#4C4C53", image=ctk.CTkImage(light_image=(p:=self.visibility[1]), size=p.size), command=lambda: self.toggle_show(self.password, self.hide), anchor="center", hover_color="#4C4C53")
        self.hide.grid(row=0, column=2, padx=(0, 5), pady=(3, 0))
        
        button_width = 56
        self.login_button = ctk.CTkButton(self, login_panel.get_dim()[0] - login_panel.padding[0] - login_panel.padding[1], button_width, 10, bg_color="#36363B", fg_color="#d81f26", text="Login", font=("Inter Black", 20), text_color="white", hover_color="#b41f24", command=self.button_callback)
        self.login_button.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=login_panel.get_pos()[1] + login_panel.get_dim()[1] - login_panel.padding[3] - button_width)
        
        self.animate()
    
    def animate(self):
        for x in self.images:
            x.slide()
            if x.get_pos()[0] >= self.width / self.images_count + self.width - x.get_size()[0]:
                x.goto(-x.get_size()[0], "")
        
        self.after(16, self.animate)
        
    def toggle_show(self, entry: ctk.CTkEntry, button: ctk.CTkButton):
        current = entry.cget("show")
        if current != "":
            entry.configure(show="")
            button.configure(image=ctk.CTkImage(light_image=(p:=self.visibility[1])))
        else:
            entry.configure(show="•")
            button.configure(image=ctk.CTkImage(light_image=(p:=self.visibility[0])))

    def button_callback(self):
        user = self.email.get()
        password = self.password.get()
        success = self.login_switch((user, password))
        if not success:
            print("Incorrect username, email or password. Please try again.")


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

class WatchFrame(ctk.CTkFrame):
    def __init__(self, master, media: Union[Movie, Anime, Show, AnimeMovie], favourite_callback):
        super().__init__(master, fg_color="transparent")
        self.media = media
        self.favourite_callback = favourite_callback
        
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1), weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=0)
        self.build_ui()
    
    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text=self.media.get_title(), font=TITLE_FONT)
        self.poster_label = ctk.CTkLabel(self, image=self.media.get_poster(BIG_POSTER_SIZE), text="")
        overview = self.media.get_overview()[:300]
        if(len(self.media.get_overview())>=300):
            overview+="..."
        self.overview_textbox = ctk.CTkTextbox(self, wrap="word", fg_color="transparent", font=SMALL_FONT)
        self.overview_textbox.insert("0.0", self.media.get_overview())
        self.overview_textbox.configure(state="disabled")
        self.star_button = ctk.CTkButton(self, text="☆ Add to favourites", command=self.toggle_favourite, font=TEXT_FONT)

        self.title_label.grid(row=0, column=0, pady=(10, 10), padx=0)
        self.poster_label.grid(row=1, column=0, pady=(10, 10), padx=(10, 10), sticky="nsew")
        self.overview_textbox.grid(row=2, column=0, pady=(10, 10), padx=(10, 10), sticky="nsew")
        self.star_button.grid(row=3, column=0, pady=(10, 10))

    def switch_media(self, new_media):
        self.media = new_media

        self.title_label.configure(text=self.media.get_title())
        self.poster_label.configure(image=self.media.get_poster(BIG_POSTER_SIZE))
        overview = self.media.get_overview()[:300]
        if(len(self.media.get_overview())>=300):
            overview+="..."
        self.overview_textbox.configure(state="normal")
        self.overview_textbox.delete("0.0", "end")
        self.overview_textbox.insert("0.0", self.media.get_overview())
        self.overview_textbox.configure(state="disabled")

    def toggle_favourite(self):
        self.favourite_callback(self.media)

    def set_starred_state(self, starred):
        if starred:
            self.star_button.configure(text="[★] Remove from favourites")
        else:
            self.star_button.configure(text="[☆] Add to favourites")

class Mediabar(ctk.CTkScrollableFrame):
    def __init__(self, master, name,  media, watch_function):
        super().__init__(master, orientation="horizontal")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.name = name
        self.media = media
        self.images = []
        self.watch_function = watch_function
        self.build_ui()

    def build_ui(self):
        self.buttons = []
        for i, media in enumerate(self.media):
            assert type(media) in [Movie, Show, Anime, AnimeMovie]
            media_image = media.get_poster()
            media_button = ctk.CTkButton(self, image=media_image, text="", fg_color="transparent", command=lambda i=i: self.button_callback(i))
            self.images.append(media_image)
            self.buttons.append(media_button)
            media_button.grid(row=0, column=i, sticky="ew", pady=0, padx=(10, 10))
    
    def button_callback(self, index):
        self.watch_function(self.media[index])

    def update_media(self, new_media):
        self.media = new_media
        for button in self.buttons:
            button.grid_forget()
        self.build_ui()

class LabelledMediabar(ctk.CTkFrame):
    def __init__(self, master, name, media, watch_function):
        super().__init__(master)
        self.name = name
        self.media = media
        self.media_bar = Mediabar(self, name, self.media, watch_function)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.build_ui()

    def build_ui(self):
        self.label = ctk.CTkLabel(self, text=self.name, font=TEXT_FONT)
        self.label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.media_bar.grid(row=1, column=0, sticky="nsew", pady=0)

    def update_media(self, new_media):
        self.media_bar.update_media(new_media)

class HomeFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, name, watch_function):
        super().__init__(master, fg_color="transparent")
        self.name = name

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3, 4, 5), weight=1)
        self.movie_bar_1 = LabelledMediabar(self, "Recommended movies", [Movie(random.choice(jsons["movie"]), POSTER_SIZE) for x in range(20)], watch_function)
        self.movie_bar_2 = LabelledMediabar(self, "TV shows", [Show(random.choice(jsons["tv"]), POSTER_SIZE) for x in range(5)], watch_function)
        self.movie_bar_3 = LabelledMediabar(self, "Anime", [Anime(random.choice(jsons["anime"]), POSTER_SIZE) for i in range(5)], watch_function)
        self.movie_bar_4 = LabelledMediabar(self, "Anime movies", [AnimeMovie(random.choice(jsons["anime_movie"]), POSTER_SIZE) for x in range(5)], watch_function) 
        self.movie_bar_5 = LabelledMediabar(self, "Explore(not random)", [Movie(jsons["movie"][i], POSTER_SIZE) for i in range(5)], watch_function)

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
        self.grid_columnconfigure((0, 1, 2), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.restrictions_map = RESTRICTIONS_MAP
        self.build_ui()

    def build_ui(self):
        self.filter_by = ctk.CTkOptionMenu(self, values=FILTER_SORT_OPTIONS, command=self.filter_change)
        self.filter_by_restriction_menu = ctk.CTkOptionMenu(self, values=self.restrictions_map["any"])
        self.sort_by = ctk.CTkOptionMenu(self, values=FILTER_SORT_OPTIONS)
        self.type = ctk.CTkOptionMenu(self, values=["Movie", "TV Show", "Anime", "Anime movie"])

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

class SearchFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, watch_function):
        super().__init__(master, fg_color="transparent", orientation="vertical")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)
        self.results_bar = LabelledMediabar(self, "Results", [Movie({}, POSTER_SIZE) for _ in range(10)], watch_function)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Search", font=TITLE_FONT)
        self.filter_sort_frame = FilterSortFrame(self)
        self.a_button = ctk.CTkButton(self, text="Search button", command=self.button_callback, font=TEXT_FONT)

        self.title_label.grid(row=0, column=0, sticky="nsew")
        self.filter_sort_frame.grid(row=1, column=0)
        self.a_button.grid(row=2, column=0)
        self.results_bar.grid(row=3, column=0, sticky="nsew")

    def button_callback(self):
        new_movies = get_media("movie", *self.filter_sort_frame.get_filter(), self.filter_sort_frame.get_sort(), count=10)
        self.results_bar.update_media(new_movies)

class StarredFrame(ctk.CTkFrame):
    def __init__(self, master, watch_function):
        super().__init__(master, fg_color="transparent")
        self.watch_function = watch_function
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1), weight=1)

        self.media_bar = LabelledMediabar(self, "Favourites", [], self.watch_function)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Starred movies and TV shows", font=TITLE_FONT)

        self.media_bar.grid(row=1, column=0, sticky="nsew")
        self.title_label.grid(row=0, column=0, sticky="nsew", pady=(10, 10))

    def update_media(self, media):
        self.media_bar.update_media(media)

class PlaybackSettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure((0, 1), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.build_ui()

    def build_ui(self):
        self.resolution_label = ctk.CTkLabel(self, text="Default resolution", font=TEXT_FONT)
        self.resolution_combo = ctk.CTkComboBox(self, values=["Auto", "480p", "720p", "1080p"], font=TEXT_FONT)
        self.autoplay_var = tk.BooleanVar(value=True)
        self.autoplay_switch = ctk.CTkSwitch(self, text="Enable autoplay", variable=self.autoplay_var, font=TEXT_FONT)
        
        self.resolution_label.grid(row=0, column=0, pady=(10, 10), padx=(10, 10))
        self.resolution_combo.grid(row=0, column=1, pady=(10, 10), padx=(10, 10))
        self.autoplay_switch.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))

class AppearanceSettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        self.grid_columnconfigure(1, minsize=500)
        self.build_ui()

    def build_ui(self):
        self.resolution_label = ctk.CTkLabel(self, text="idk, choose something", font=TEXT_FONT)
        self.resolution_combo = ctk.CTkComboBox(self, values=["you must choose me or else"], font=TEXT_FONT)
        self.unnecessary_var = tk.BooleanVar(value=True)
        self.necessary_var = tk.BooleanVar(value=True)
        self.unnecessary_switch = ctk.CTkSwitch(self, text="Allow unnecessary cookies", variable=self.unnecessary_var, font=TEXT_FONT, command=self.cookie_command)
        self.necessary_switch = ctk.CTkSwitch(self, text="Allow necessary cookies", variable=self.necessary_var, font=TEXT_FONT, state="disabled")
        
        self.resolution_label.grid(row=0, column=0, pady=(10, 10), padx=(10, 10))
        self.resolution_combo.grid(row=0, column=1, pady=(10, 10), padx=(10, 10), sticky="ew")
        self.unnecessary_switch.grid(row=1, column=0, pady=(10, 10), padx=(10, 10))
        self.necessary_switch.grid(row=2, column=0, pady=(10, 10), padx=(10, 10))
    
    def cookie_command(self):
        if self.unnecessary_switch.get() == 0:
            self.after(300, lambda: self.unnecessary_switch.toggle())

class SettingsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Settings", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew", pady=(10, 10))

        self.tabs= ctk.CTkTabview(self)

        self.tabs.add("Playback")
        self.playback_tab = self.tabs.tab("Playback")
        self.playback_frame = PlaybackSettingsFrame(self.playback_tab)
        self.playback_frame.grid(row=0, column=0)

        self.tabs.add("Appearance")
        self.appearance_tab = self.tabs.tab("Appearance")
        self.appearance_frame = AppearanceSettingsFrame(self.appearance_tab)
        self.appearance_frame.grid(row=0, column=0)

        self.tabs.grid(row=1, column=0, sticky="nsew")

class AccountFrame(ctk.CTkFrame):
    def __init__(self, master, name):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.name = name
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Account", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew", pady=(10, 10))
        self.tabs= ctk.CTkTabview(self)
        self.tabs.add("Account")
        self.tabs.add("Profile")
        self.tabs.grid(row=1, column=0, sticky="nsew")

    def change_name(self, new_name):
        self.name = new_name
        self.title_label.configure(text=f"Account: {self.name}")

class MovieBrowser(ctk.CTkFrame):
    def __init__(self, master, name, quit):
        super().__init__(master)
        self.grid_columnconfigure(0, minsize=100)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        self.quit = quit
        self.name = name
        self.starred_media = []

        self.home_frame = HomeFrame(self, self.name, self.watch_media)
        self.search_frame = SearchFrame(self, self.watch_media)
        self.star_frame = StarredFrame(self, self.watch_media)
        self.settings_frame = SettingsFrame(self)
        self.account_frame = AccountFrame(self, self.name)
        self.watch_frame = WatchFrame(self, Movie({}), self.toggle_favourite)

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

    def watch_media(self, media: Union[Movie, Anime, Show, AnimeMovie]):
        self.watch_frame.switch_media(media)
        self.watch_frame.set_starred_state(self.is_starred(media))
        self.switch_frame(self.watch_frame)

    def change_name(self, new_name: str):
        self.home_frame.change_name(new_name)
        self.account_frame.change_name(new_name)

    def switch_frame(self, new_frame):
        self.current_frame.grid_forget()
        new_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", pady=(10, 10), padx=(10, 10))
        self.current_frame = new_frame

    def is_starred(self, media):
        return any([m.get_id() == media.get_id() for m in self.starred_media])
    
    def toggle_favourite(self, media):
        if self.is_starred(media):
            self.starred_media = [m for m in self.starred_media if m.get_id() != media.get_id()]
        else:
            self.starred_media.append(media)

        self.star_frame.update_media(self.starred_media)
        self.watch_frame.set_starred_state(self.is_starred(media))

class StreamingApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("streaming service")
        self.geometry("1280x720")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.user = ""
        self.account_manager = AccountManager(accounts_path)
        
        self.build_ui()

    def build_ui(self):
        self.login_frame = LoginFrame(self, self.handle_login)
        self.login_frame.grid(row=0, column=0, sticky="nsew")
        self.loading_frame = LoadingScreen(self, loading_text="Loading...")
        self.browse_frame = MovieBrowser(self, self.user, quit=self.quit)

    def switch_frame(self, frame1: ctk.CTkFrame, frame2: ctk.CTkFrame):
        frame1.grid_forget()
        frame2.grid(row=0, column=0, sticky="nsew")

    def handle_login(self, userdata: tuple[str, str]) -> bool:
        username_email, password = userdata

        accounts = self.account_manager.load_accounts()
        logged_in_user = None
        for account in accounts:
            if account.email.strip().lower() == username_email.lower() or account.username == username_email:
                if account.check_password(password):
                    logged_in_user = account
                    break

        if logged_in_user:
            username = logged_in_user.username
            password = logged_in_user.get_password() # FIXME: encapsulation leak
            print(f"Logging in as {username} with password {password}")
            self.login_switch(username)
            return True
        else:
            # FIXME: 
            print("Incorrect details.")
            return False

    def login_switch(self, user):
        self.switch_frame(self.login_frame, self.loading_frame)
        self.user = user
        self.browse_frame.change_name(user)
        self.after(500, lambda:self.switch_frame(self.loading_frame, self.browse_frame))

    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = StreamingApp()
    app.mainloop()