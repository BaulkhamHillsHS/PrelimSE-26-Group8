from datetime import datetime, timedelta
from typing import Union
import customtkinter as ctk
from PIL import Image
import os
import json
from pathlib import Path
from enum import Enum
import csv
from datetime import datetime, timedelta

TITLE_FONT = ("Inter", 35, "bold")
TEXT_FONT = ("Arial", 20)
SMALL_FONT = ("Arial", 17)
TYPEWRITER_FONT = ("Courier New", 14)
BOLD_TYPEWRITER_FONT = ("Courier New", 18, "bold")
BIG_TYPEWRITER_FONT = ("Courier New", 24)

POSTER_SIZE = (96, 144)
MEDIUM_POSTER_SIZE = (160, 240)
BIG_POSTER_SIZE = (320, 480)

FILTER_SORT_OPTIONS = ["any", "score rating", "length", "popularity"]
RESTRICTIONS_MAP = {
            "any": [""],
            "score rating": [">8.5", ">8", ">7.5", ">7"],
            "length": ["<75m", "<90m", "<120m", ">75m", ">90m", ">120m"],
            "popularity": [">200", ">175", ">150", ">100", ">50"]
        }

PRIMARY_COLOUR = "#ecb050"
SECONDARY_COLOUR = "#f5e35e"

root = Path(__file__).resolve().parent
resource_path = os.path.join(root, "resource")
posters_path = os.path.join(resource_path, "posters")

accounts_path = os.path.join(resource_path, "accounts.csv")
theme_path = os.path.join(resource_path, "theme.json")
viewing_txt_path = os.path.join(resource_path, "viewing_data.txt")

def read_json(filepath: str):
    assert os.path.exists(filepath)
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def write_json(obj, filepath: str, encoding="utf-8"):
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
    
class PaymentDialog(ctk.CTkToplevel):
    def __init__(self, master, current_plan_name: str, success_callback, payment_info: str=""):
        super().__init__(master)
        self.title("Payment Checkout")
        self.geometry("400x500")
        self.resizable(False, False)

        # Force interaction
        self.transient(master)
        self.grab_set()

        self.on_success = success_callback
        self.current_plan = current_plan_name
        self.payment_info = payment_info

        self.price_dict = {"FreePlan": 0, "StandardPlan": 9, "PremiumPlan": 15}

        self.grid_columnconfigure((0, 1), weight=1)
        self.build_ui()

    def build_ui(self):
        self.main_label = ctk.CTkLabel(self, text=f"Upgrade Subscription Plan", font=BOLD_TYPEWRITER_FONT)
        self.select_label = ctk.CTkLabel(self, text="Select Tier", font=BOLD_TYPEWRITER_FONT)
        self.available_options = []
        if self.current_plan == "FreePlan":
            self.available_options = ["Standard Plan ($8.99/month)", "Premium Plan ($14.99/month)"]
        elif self.current_plan == "StandardPlan":
            self.available_options = ["Premium Plan ($14.99/month, additional $6 dollars) [SAVE 8 DOLLARS BUYING NOW]"]
        else:
            self.available_options = ["Already at highest tier"]

        self.plan_dropdown = ctk.CTkOptionMenu(self, values=self.available_options, font=SMALL_FONT, height=38, button_color=PRIMARY_COLOUR, button_hover_color=SECONDARY_COLOUR, command=self.update_price_display)
        self.price_label = ctk.CTkLabel(self, text="", font=BIG_TYPEWRITER_FONT)
        self.update_price_display(self.plan_dropdown.get())

        self.card_entry = ctk.CTkEntry(self, placeholder_text="Card number", font=SMALL_FONT, height=40)
        self.expiry_entry = ctk.CTkEntry(self, placeholder_text="MM/YY", font=SMALL_FONT, height=40)
        self.cvv_entry = ctk.CTkEntry(self, placeholder_text="CVV", font=SMALL_FONT, height=40, show="*")
        self.error_label = ctk.CTkLabel(self, text="", text_color="red", font=SMALL_FONT)

        if self.payment_info and self.payment_info.strip() != "":
            parts = [p.strip() for p in self.payment_info.split("|")]
            if len(parts)>=1:
                self.card_entry.insert(0, parts[0])
            if len(parts)>=2:
                self.expiry_entry.insert(0, parts[1])
            if len(parts)>=3:
                self.cvv_entry.insert(0, parts[2])
        
        self.pay_button = ctk.CTkButton(self, text="Confirm Payment", font=BOLD_TYPEWRITER_FONT, fg_color=PRIMARY_COLOUR, text_color="white", hover_color=SECONDARY_COLOUR, command=self.process_payment)
        self.cancel_button = ctk.CTkButton(self, text="Cancel", font=SMALL_FONT, height=40, fg_color="transparent", command=self.destroy)
        
        self.main_label.grid(row=0, column=0, columnspan=2, pady=(30, 5), padx=20, sticky="ew")
        self.select_label.grid(row=1, column=0, columnspan=2, pady=(10, 2), padx=40, sticky="w")
        self.plan_dropdown.grid(row=2, column=0, columnspan=2, pady=(0, 15), padx=40, sticky="ew")
        self.price_label.grid(row=3, column=0, columnspan=2, pady=(0, 15), padx=40, sticky="ew")
        
        self.card_entry.grid(row=4, column=0, columnspan=2, pady=10, padx=40, sticky="ew")
        self.expiry_entry.grid(row=5, column=0, pady=10, padx=(40, 5), sticky="ew")
        self.cvv_entry.grid(row=5, column=1, pady=10, padx=(5, 40), sticky="ew")
        
        self.error_label.grid(row=6, column=0, columnspan=2, pady=5, padx=20, sticky="ew")
        self.pay_button.grid(row=7, column=0, columnspan=2, pady=(15, 10), padx=40, sticky="ew")
        self.cancel_button.grid(row=8, column=0, columnspan=2, pady=5, padx=40, sticky="ew")

    def update_price_display(self, selected_choice: str):
        if "Standard" in selected_choice:
            self.price_label.configure(text="Total: $8.99/month")
        elif "additional $6" in selected_choice:
            self.price_label.configure(text="Total Upgrade Fee: $6.00")
        elif "Premium Plan" in selected_choice:
            self.price_label.configure(text="Total: $14.99/month")
        else:
            self.price_label.configure(text="No active transaction amount due.")

    def process_payment(self):
        choice = self.plan_dropdown.get()
        if "Already" in choice:
            self.error_label.configure(text="You are already on the highest tier.")
            return

        card = self.card_entry.get().replace(" ", "")
        expiry = self.expiry_entry.get().strip()
        cvv = self.cvv_entry.get().strip()

        if len(card)<15 or not card.isdigit():
            self.error_label.configure(text="Invalid card number(15 digits)")
            return
        if "/" not in expiry or len(expiry)!=5:
            self.error_label.configure(text="Invalid expiry date (MM/YY)")
            return
        if len(cvv)!=3 or not cvv.isdigit():
            self.error_label.configure(text="Invalid CVV.")
            return
        

        
        chosen_plan = "StandardPlan" if "Standard" in choice else "PremiumPlan"
        self.on_success(chosen_plan)
        self.destroy()

class WatchHistory(ctk.CTkToplevel):
    def __init__(self, parent, username, watch_history_list, text_path):
        super().__init__(parent)
        self.username = username
        self.watch_history_list = watch_history_list
        self.text_path = text_path

        self.geometry("400x500")
        self.title("Watch History")
        self.resizable(False, False)
        self.attributes("-topmost", True)

        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=400, height=500)
        self.scrollable_frame.pack(fill="both", expand=True)
        self.build_ui()

    def build_ui(self):
        self.logo_frame = ctk.CTkFrame(self.scrollable_frame, fg_color="transparent")
        self.logo_frame.pack(pady=20)
        self.real_logo = ctk.CTkImage(images["small_logo"], size=(64, 64))
        self.logo_label = ctk.CTkLabel(self.logo_frame, image=self.real_logo, text="")
        self.logo_label.pack(side="left", padx=(0, 10))

        self.name_label = ctk.CTkLabel( self.logo_frame, text="BreakFlix", text_color="white", font=("Inter", 25, "bold"))
        self.name_label.pack(side="left")

        self.create_history()
        self.create_txt()

    def create_history(self):
        self.receipt = []
        self.receipt.append("-" * 36)

        if self.watch_history_list:
            for item in self.watch_history_list:
                self.receipt.append(f"{item}\n")
        else:
            self.receipt.append("No Movies watched\n")

        self.receipt.append(f"ACCOUNT: {self.username.upper()}")
        self.receipt.append("-" * 36)
        receipt_display = ctk.CTkLabel(self.scrollable_frame, text="\n".join(self.receipt), font=("Courier New", 14), justify="left")
        receipt_display.pack(pady=10)

    def create_txt(self):
        bank_name = "            BreakFlix            \n"
        with open(self.text_path, "w", encoding="utf-8") as file:
            file.write(bank_name + "\n".join(self.receipt))
    
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
    
    def set_payment_info(self, new_payment_info):
        self.__payment_info = new_payment_info
    
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
        case "length":
            return data.get("runtime", 0)
        case "popularity":
            return data.get("popularity", 0)
        case _:
            return data.get(attribute, default)

def restriction_check(filter: str, restriction: str, media_data: dict, is_adult_profile=True):
    if not is_adult_profile:
        rating = None
        for key in ["rating", "content_rating", "certification"]:
            if key in media_data:
                rating = str(media_data[key]).strip().upper()
                break
        if not rating or rating == "" or rating == "UNRATED":
            return False
        
        allowed_child_ratings = ["G", "PG", "TV-Y", "TV-Y7", "TV-G", "TV-PG"]

        if rating not in allowed_child_ratings:
            return False
    
    assert filter in FILTER_SORT_OPTIONS
    assert restriction in RESTRICTIONS_MAP[filter]
    match filter:
        case "any":
            return True
        case "score rating":
            media_score = media_get_attribute(media_data, filter, 0) 
            required = float(restriction[1:])
            return media_score>=required
        case "length":
            media_length = media_get_attribute(media_data, filter, 0)
            required = int(restriction[1:-1])
            if restriction[0]=="<":
                return media_length<required
            else:
                return media_length>required
        case "popularity":
            media_popularity = media_get_attribute(media_data, "popularity", 0)
            required = int(restriction[1:])
            return media_popularity>=required

def get_media(media_type: str, filter_by: str, restriction: str, sort_by: str, count: int, ascending: bool=False, search_query: str="", current_profile=None, current_account=None):
    match media_type:
        case "movie":
            media_dict = jsons["movie"]
            popularity_bounds = (60, 150)
        case "tv_show" | "tv show":
            media_dict = jsons["tv"]
            popularity_bounds = (80, 200)
        case "anime_movie" | "anime movie":
            media_dict = jsons["anime_movie"]
            popularity_bounds = (30, 80)
        case "anime":
            media_dict = jsons["anime"]
            popularity_bounds = (40, 100)
        case _:
            raise ValueError()
        
    assert filter_by, sort_by in FILTER_SORT_OPTIONS
    assert restriction in RESTRICTIONS_MAP[filter_by]
    out = []
    free_max, standard_max = popularity_bounds

    for media in media_dict:
        # SUBSCRIPTION POPULARITY CHECK
        popularity = media.get("popularity", 0)
        if current_account:
            plan = current_account.subscription_plan.value
            if plan=="FreePlan" and popularity>free_max:
                continue
            if plan=="StandardPlan" and popularity>standard_max:
                continue

        # ADULT CHECK
        is_adult = True
        if current_profile is not None:
            is_adult = current_profile.is_adult

        # SEARCH QUERY CHECK
        if search_query:
            title = media.get("title", media.get("name", "")).lower()
            if search_query.lower() not in title:
                continue

        if restriction_check(filter_by, restriction, media, is_adult_profile=is_adult):
            out.append(media)

    if sort_by!="any":
        out.sort(key=lambda x: media_get_attribute(x, sort_by, 0), reverse=not ascending)

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
        return self.canvas.tk.call(self.canvas._w, "coords", self.id) # type: ignore
    
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
