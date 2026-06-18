from datetime import datetime
from typing import Union
import customtkinter as ctk
from PIL import Image
import os
import json
from pathlib import Path
from enum import Enum
import csv

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

PRIMARY_COLOUR = "#ecb050"
SECONDARY_COLOUR = "#f5e35e"


root = Path(__file__).resolve().parent
resource_path = os.path.join(root, "resource")
posters_path = os.path.join(resource_path, "posters")

accounts_path = os.path.join(resource_path, "accounts.csv")
theme_path = os.path.join(resource_path, "theme.json")

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

image_names = [
          # HENRY STUFF
          "settings_icon",
          "home_icon",
          "search_icon",
          "star_icon",
          "quit_icon",
          "account_icon",
          "small_logo",
          # BEN STUFF
          "blind",
          "eye",
          "lock",
          "person",
          "wide_logo"
          ]

images = {}

for name in image_names:
    image_path = os.path.join(resource_path, name+".png")
    image = Image.open(image_path)
    images[name] = image

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

class Season():
    def __init__(self, media_data: dict, dimensions=POSTER_SIZE):
        self.media_data = media_data
        self.season_number = self.get_data("season_number", 0)
        self.dimensions = dimensions
        #self.pillow_image = Image.open(os.path.join(posters_path, f"s_{self.get_id()}.jpg")) # FIXME: incomplete impl
        #self.poster = ctk.CTkImage(self.pillow_image, size=dimensions)
        self.episode_count = int(self.get_data("episode_count", 0)) # 
    
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
    
def media_get_attribute(data, attribute, default):
    match attribute:
        case "score_rating" | "score rating":
            return data["vote_average"]
        case "age_rating" | "age rating":
            raise ValueError() # FIXME:
        case "length":
            return data["runtime"]
        case "genre":
            return data["genres"]
        case "popularity":
            return data["popularity"]
        case _:
            return data.get(attribute, default)

def restriction_check(filter: str, restriction: str, media_data: dict):
    assert filter in FILTER_SORT_OPTIONS
    assert restriction in RESTRICTIONS_MAP[filter]
    match filter:
        case "any":
            return True
        case "score rating":
            media_score = media_get_attribute(media_data, filter, 0) 
            required = float(restriction[1:])
            return media_score>=required
        case "age rating":
            raise ValueError() # No age ratings yet... FIXME:
        case "length":
            media_length = media_get_attribute(media_data, filter, 0)
            required = float(restriction[1:])
            required = int(restriction[1:-1])
            if restriction[0]=="<":
                return media_length<required
            else:
                return media_length>required
        case "genre":
            media_genres = media_get_attribute(media_data, filter, [])
            for genre in media_genres:
                if genre["name"]==restriction:
                    return True
            return False
        case "popularity":
            media_popularity = media_get_attribute(media_data, "popularity", 0)
            required = int(restriction[1:])
            return media_popularity>=required
    raise ValueError()  # FIXME: debug, delete later

def get_media(media_type: str, filter_by: str, restriction: str, sort_by: str, count: int, decreasing: bool=False):
    match media_type:
        case "movie":
            media_dict = jsons["movie"]
        case "tv_show" | "tv show":
            media_dict = jsons["tv"]
        case "anime_movie" | "anime movie":
            media_dict = jsons["anime_movie"]
        case "anime":
            media_dict = jsons["anime"]
        case _:
            raise ValueError()
        
    assert filter_by, sort_by in FILTER_SORT_OPTIONS
    assert restriction in RESTRICTIONS_MAP[filter_by]
    out = []
    for media in media_dict:
        if restriction_check(filter_by, restriction, media):
            out.append(media)

    if sort_by!="any":
        if sort_by=="genre":
            out.sort(key=lambda x: media_get_attribute(x, sort_by, 0)[0]["name"] if bool(len(media_get_attribute(x, sort_by, 0))) else "", reverse=decreasing) # type: ignore FIXME: SO SCUFFED
        else:
            out.sort(key=lambda x: media_get_attribute(x, sort_by, 0), reverse=decreasing)

    match media_type:
        case "movie":
            return [Movie(x) for x in out[:count]]
        case "tv_show" | "tv show":
            return [Show(x) for x in out[:count]]
        case "anime_movie" | "anime movie":
            return [AnimeMovie(x) for x in out[:count]]
        case "anime":
            return [Anime(x) for x in out[:count]]

def pretty_time(minutes: int, clock=False):
    if clock:
        return f"{minutes//60}:{minutes%60}"
    else:
        return f"{minutes//60}h{minutes%60}m"
    
def get_current_time():
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")