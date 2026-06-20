from typing import Union
from PIL import Image
from PIL import ImageTk, ImageEnhance
import random
from PIL import Image
import customtkinter as ctk
import tkinter as tk

from utils import TITLE_FONT, TEXT_FONT, SMALL_FONT, TYPEWRITER_FONT
from utils import POSTER_SIZE, MEDIUM_POSTER_SIZE, BIG_POSTER_SIZE
from utils import FILTER_SORT_OPTIONS, RESTRICTIONS_MAP
from utils import PRIMARY_COLOUR, SECONDARY_COLOUR

from utils import ImageCell, Panel
from utils import SubscriptionPlan
from utils import accounts_path, theme_path, viewing_txt_path
from utils import images, jsons
from utils import Movie, Show, Anime, AnimeMovie
from utils import AccountManager, WatchHistory, PaymentDialog
from utils import get_media
from utils import pretty_time, get_current_time

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme(theme_path)

class LoadingFrame(ctk.CTkFrame):
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
        
        pil_image = images["small_logo"]
        pil_image_dark = ImageEnhance.Brightness(images["small_logo"]).enhance(0.6)#.transpose(Image.Transpose.FLIP_LEFT_RIGHT)

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
        
        title = images["wide_logo"]
        title_pad = 30
        
        self.asdf = ImageTk.PhotoImage(title.resize(((w_x:=login_panel.get_udim()[0] - 2 * title_pad), int(title.size[1] / title.size[0] * w_x))))
        self.netflix = self.canvas.create_image(login_panel.pos[0] + login_panel.padding[0] + title_pad, login_panel.pos[1] + login_panel.padding[2] + title_pad, image=self.asdf, anchor="nw")
        
        self.email_frame = ctk.CTkFrame(self, login_panel.get_udim()[0], 56, 10, bg_color="#36363B", fg_color="#4C4C53", border_width=2, border_color="#6F6F70")
        self.email_frame.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=self.canvas.bbox(self.netflix)[3] + 40)
        self.email_frame.rowconfigure(0, weight=1)
        self.email_frame.columnconfigure(1, weight=1)
        self.email_frame.grid_propagate(False)
        
        self.email = ctk.CTkEntry(self.email_frame, font=main_font, placeholder_text="Email or mobile number", border_width=0, fg_color="#4C4C53", text_color="#98989B")
        self.email.grid(row=0, column=1, sticky="nsew", pady=2, padx=(0, 15))
        self.person_icon = ctk.CTkLabel(self.email_frame, image=ctk.CTkImage(light_image=(p:=images["person"]), size=p.size), text="")
        self.person_icon.grid(row=0, column=0, padx=(12, 10))
        
        self.password_frame = ctk.CTkFrame(self, login_panel.get_udim()[0], 56, 10, bg_color="#36363B", fg_color="#4C4C53", border_width=2, border_color="#6F6F70")
        self.password_frame.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=self.canvas.bbox(self.netflix)[3] + 40 + 56 + 24)
        self.password_frame.rowconfigure(0, weight=1)
        self.password_frame.columnconfigure(1, weight=1)
        self.password_frame.grid_propagate(False)
        
        self.password = ctk.CTkEntry(self.password_frame, font=main_font, placeholder_text="Password", border_width=0, fg_color="#4C4C53", show="•", text_color="#98989B")
        self.password.grid(row=0, column=1, sticky="nsew", pady=2, padx=(0, 15))

        self.lock_icon = ctk.CTkLabel(self.password_frame, image=ctk.CTkImage(light_image=(p:=images["lock"]), size=p.size), text="")
        self.lock_icon.grid(row=0, column=0, padx=(12, 10))

        self.password_visible = False
        
        self.eye_icon = ctk.CTkImage(images["eye"], size=images["eye"].size)
        self.blind_icon = ctk.CTkImage(images["blind"], size=images["blind"].size)
        self.hide = ctk.CTkButton(self.password_frame, width=0, height=40, text="", fg_color="#4C4C53", image=self.blind_icon, command=lambda: self.toggle_show(self.password, self.hide), anchor="center", hover_color="#4C4C53")
        self.hide.grid(row=0, column=2, padx=(0, 5), pady=(3, 0))
        
        button_width = 56
        self.login_button = ctk.CTkButton(self, login_panel.get_dim()[0] - login_panel.padding[0] - login_panel.padding[1], button_width, 10, bg_color="#36363B", fg_color=PRIMARY_COLOUR, text="Login", font=("Inter Black", 20), text_color="white", hover_color=SECONDARY_COLOUR, command=self.button_callback)
        self.login_button.place(x=login_panel.get_pos()[0] + login_panel.padding[0], y=login_panel.get_pos()[1] + login_panel.get_dim()[1] - login_panel.padding[3] - button_width)
        
        self.incorrect_password_label = self.canvas.create_text(self.width*0.5, self.height*0.65, text="Incorrect username, \nemail, or password.\nPlease try again", fill="#FF0000", state="hidden", font=SMALL_FONT, justify="center")
        
        self.email.bind("<Return>", lambda a: self.button_callback())
        self.password.bind("<Return>", lambda a: self.button_callback())

        self.animate()
    
    def animate(self):
        for x in self.images:
            x.slide()
            if x.get_pos()[0] >= self.width / self.images_count + self.width - x.get_size()[0]:
                x.goto(-x.get_size()[0], "")
        
        self.after(16, self.animate)
        
    def toggle_show(self, entry: ctk.CTkEntry, button: ctk.CTkButton):
        if not self.password_visible:
            entry.configure(show="")
            button.configure(image=self.eye_icon)
        else:
            entry.configure(show="•")
            button.configure(image=self.blind_icon)
        self.password_visible = not self.password_visible

    def button_callback(self):
        user = self.email.get()
        password = self.password.get()
        success = self.login_switch((user, password))
        if not success:
            self.canvas.itemconfigure(self.incorrect_password_label, state="normal")

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
        
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=3)
        self.grid_rowconfigure(3, weight=0)
        self.build_ui()
    
    def build_ui(self):
        vote_average = self.media.get_data("vote_average", "N/A")
        runtime = pretty_time(self.media.get_runtime())
        if isinstance(self.media, (Anime, Show)):
            episode_count = sum([season.episode_count for season in self.media.get_seasons()])
        else:
            episode_count = "N/A"
        genres = ", ".join(genre["name"] for genre in self.media.get_data("genres", []))
        tagline = self.media.get_data("tagline", "")

        self.title_label = ctk.CTkLabel(self, text=self.media.get_title(), font=TITLE_FONT)
        self.poster_label = ctk.CTkLabel(self, image=self.media.get_poster(BIG_POSTER_SIZE), text="")
        overview = self.media.get_overview()[:300]
        if(len(self.media.get_overview())>=300):
            overview+="..."

        self.info_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.overview_textbox = ctk.CTkTextbox(self.info_frame, wrap="word", fg_color="transparent", font=SMALL_FONT)
        self.overview_textbox.insert("0.0", self.media.get_overview())
        self.overview_textbox.configure(state="disabled")
        self.star_button = ctk.CTkButton(self.info_frame, text="☆ Add to favourites", command=self.toggle_favourite, font=TEXT_FONT)
        self.vote_label = ctk.CTkLabel(self.info_frame, text=f"Vote average: {vote_average}", font=TEXT_FONT, anchor="w")
        self.runtime_label = ctk.CTkLabel(self.info_frame, text=f"runtime: {runtime}", font=TEXT_FONT, anchor="w")
        self.episode_label = ctk.CTkLabel(self.info_frame, text=f"Episodes: {episode_count}", font=TEXT_FONT, anchor="w")
        self.genre_label = ctk.CTkLabel(self.info_frame, text=f"Genres: {genres}", font=TEXT_FONT, anchor="w")
        self.tagline_label = ctk.CTkLabel(self.info_frame, text=f"Tagline:\n{tagline}", anchor="w", wraplength=400, justify="left", font=SMALL_FONT)

        self.info_frame.grid_columnconfigure(0, weight=1)
        self.info_frame.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=1)
        self.vote_label.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=(10, 10))
        self.runtime_label.grid(row=1, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))
        self.episode_label.grid(row=2, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))
        self.genre_label.grid(row=3, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))
        self.tagline_label.grid(row=4, column=0, sticky="nsew", pady=(10, 10), padx=(10, 10))
        self.overview_textbox.grid(row=5, column=0, pady=(10, 10), padx=(10, 10), sticky="nsew")
        self.star_button.grid(row=6, column=0, pady=(10, 10), columnspan=2)

        self.title_label.grid(row=0, column=0, columnspan=2, pady=(10, 10), padx=0)
        self.poster_label.grid(row=1, column=0, pady=(10, 10), padx=(10, 10), sticky="nsew")
        self.info_frame.grid(row=1, column=1, pady=(10, 10), padx=(10, 10), sticky="nsew")

    def switch_media(self, new_media):
        self.media = new_media

        vote_average = self.media.get_data("vote_average", "N/A")
        runtime = pretty_time(self.media.get_runtime())
        if isinstance(self.media, (Anime, Show)):
            episode_count = sum([season.episode_count for season in self.media.get_seasons()])
        else:
            episode_count = "N/A"
        genres = ", ".join(genre["name"] for genre in self.media.get_data("genres", []))
        tagline = self.media.get_data("tagline", "N/A")

        self.title_label.configure(text=self.media.get_title())
        self.poster_label.configure(image=self.media.get_poster(BIG_POSTER_SIZE))
        overview = self.media.get_overview()[:300]
        if(len(self.media.get_overview())>=300):
            overview+="..."
        self.overview_textbox.configure(state="normal")
        self.overview_textbox.delete("0.0", "end")
        self.overview_textbox.insert("0.0", self.media.get_overview())
        self.overview_textbox.configure(state="disabled")
        self.vote_label.configure(text=f"Vote Average: {vote_average}")
        self.runtime_label.configure(text=f"Runtime: {runtime}")
        self.episode_label.configure(text=f"Episodes: {episode_count}")
        self.genre_label.configure(text=f"Genres: {genres}")
        self.tagline_label.configure(text=f'Tagline:\n{tagline}')

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
            media_image = media.get_poster(POSTER_SIZE)
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
        self.grid_rowconfigure((1, 2, 3, 4), weight=1)
        self.movie_bar = LabelledMediabar(self, "Popular Movies", [], watch_function)
        self.show_bar = LabelledMediabar(self, "TV shows", [], watch_function)
        self.anime_bar = LabelledMediabar(self, "Anime", [], watch_function)
        self.anime_movie_bar = LabelledMediabar(self, "Anime movies", [], watch_function)

        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text=f"Welcome, {self.name}", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew")
        self.movie_bar.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.show_bar.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        self.anime_bar.grid(row=3, column=0, sticky="nsew", pady=(0, 10))
        self.anime_movie_bar.grid(row=4, column=0, sticky="nsew", pady=(0, 10))

    def refresh_content(self, account, current_profile):
        movie_pool = get_media("movie", "any", "", "popularity", 40, True, search_query="", current_profile=current_profile, current_account=account)
        show_pool = get_media("tv_show", "any", "", "popularity", 40, True, search_query="", current_profile=current_profile, current_account=account)
        anime_pool = get_media("anime", "any", "", "popularity", 40, True, search_query="", current_profile=current_profile, current_account=account)
        anime_movie_pool = get_media("anime_movie", "any", "", "popularity", 40, True, search_query="", current_profile=current_profile, current_account=account)

        movies = random.sample(movie_pool, min(len(movie_pool), 15))
        shows = random.sample(show_pool, min(len(show_pool), 15))
        animes = random.sample(anime_pool, min(len(anime_pool), 15))
        anime_movies = random.sample(anime_movie_pool, min(len(anime_movie_pool), 15))

        self.movie_bar.update_media(movies)
        self.show_bar.update_media(shows)
        self.anime_bar.update_media(animes)
        self.anime_movie_bar.update_media(anime_movies)

    def change_name(self, new_name):
        self.name = new_name
        self.title_label.configure(text=f"Welcome, {self.name}")

class FilterSortFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        self.restrictions_map = RESTRICTIONS_MAP
        self.build_ui()

    def build_ui(self):
        self.filter_by = ctk.CTkOptionMenu(self, values=FILTER_SORT_OPTIONS, command=self.filter_change)
        self.filter_by_restriction_menu = ctk.CTkOptionMenu(self, values=self.restrictions_map["any"])
        self.sort_by = ctk.CTkOptionMenu(self, values=FILTER_SORT_OPTIONS)
        self.media_type = ctk.CTkOptionMenu(self, values=["Movie", "TV Show", "Anime", "Anime movie"])
        self.sort_ascending = tk.BooleanVar(value=False)
        self.sort_order_toggle = ctk.CTkSwitch(self, text="Ascending", variable=self.sort_ascending)

        self.filter_label = ctk.CTkLabel(self, text="Filter by...", font=TEXT_FONT)
        self.sort_label = ctk.CTkLabel(self, text="Sort by...", font=TEXT_FONT)
        self.media_label = ctk.CTkLabel(self, text="Media type...", font=TEXT_FONT)

        self.filter_label.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        self.sort_label.grid(row=0, column=2, padx=10, pady=10)
        self.media_label.grid(row=0, column=3, padx=10, pady=10)

        self.filter_by.grid(row=1, column=0, padx=10, pady=10)
        self.filter_by_restriction_menu.grid(row=1, column=1, padx=10, pady=10)
        self.sort_by.grid(row=1, column=2, padx=10, pady=10)
        self.media_type.grid(row=1, column=3, padx=10, pady=10)
        self.sort_order_toggle.grid(row=1, column=4, padx=10, pady=10)

    def filter_change(self, new: str):
        if new in self.restrictions_map:
            self.filter_by_restriction_menu.configure(values=self.restrictions_map[new])
            self.filter_by_restriction_menu.set(self.restrictions_map[new][0])

    def get_filter(self):
        return (self.filter_by.get(), self.filter_by_restriction_menu.get())
    
    def get_sort(self):
        return (self.sort_by.get())
    
    def get_sort_ascending(self):
        return (self.sort_ascending.get())

    def get_media_type(self):
        return (self.media_type.get())

class SearchFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, watch_function):
        super().__init__(master, fg_color="transparent", orientation="vertical")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1, 2, 3), weight=1)

        self.current_account = None
        self.current_profile = None
        self.results_bar = LabelledMediabar(self, "Results", [Movie({}, POSTER_SIZE) for _ in range(10)], watch_function)
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Search", font=TITLE_FONT)
        self.filter_sort_frame = FilterSortFrame(self)
        self.a_button = ctk.CTkButton(self, text="Search", command=self.button_callback, font=TEXT_FONT)
        self.sort_order_toggle = ctk.CTkSegmentedButton(self, values=["Descending", "Ascending"], command=self.refresh_search)
        self.sort_order_toggle.set("Descending")

        self.search_entry = ctk.CTkEntry(self, placeholder_text="Search for media...", font=TEXT_FONT, height=40)
        self.search_entry.bind("<Return>", self.refresh_search)

        self.title_label.grid(row=0, column=0, sticky="nsew", pady=(10, 10))
        self.search_entry.grid(row=1, column=0, sticky="nsew", pady=(10, 10), padx=(20, 20))
        self.filter_sort_frame.grid(row=2, column=0, pady=(10, 10))
        self.a_button.grid(row=3, column=0)
        self.results_bar.grid(row=4, column=0, sticky="nsew")

    def button_callback(self):
        new_movies = get_media(self.filter_sort_frame.get_media_type().lower(), *self.filter_sort_frame.get_filter(), self.filter_sort_frame.get_sort(), count=10, ascending=self.filter_sort_frame.get_sort_ascending(), search_query=self.search_entry.get(), current_profile=self.current_profile, current_account=self.current_account)
        self.results_bar.update_media(new_movies)

    def refresh_search(self, event=None):
        self.button_callback()

    def refresh_content(self):
        self.search_entry.delete(0, "end")
        self.results_bar.update_media([])

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
        self.resolution_combo = ctk.CTkOptionMenu(self, values=["you must choose me or else"], font=TEXT_FONT)
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
    def __init__(self, master, name, account, open_history_callback, switch_profile_callback, upgrade_callback):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.name = name
        self.account = account
        self.open_history_callback = open_history_callback
        self.switch_profile_callback = switch_profile_callback
        self.upgrade_callback = upgrade_callback
        self.build_ui()

    def build_ui(self):
        self.title_label = ctk.CTkLabel(self, text="Account options", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, sticky="nsew", pady=(10, 10))
        self.tabs= ctk.CTkTabview(self)
        self.tabs.add("Manage Profiles")
        self.tabs.add("Subscription")
        self.tabs.grid(row=1, column=0, sticky="nsew")

        self.profile_tab = self.tabs.tab("Manage Profiles")
        self.profile_tab.grid_columnconfigure((0, 1), weight=1)
        self.profile_tab.grid_rowconfigure((0, 1, 2), weight=1)
        self.profile_menu_label = ctk.CTkLabel(self.profile_tab, text="Select Profile:", font=TEXT_FONT)
        self.profile_menu_label.grid(row=0, column=0, columnspan=2, pady=(10, 10))
        self.profile_dropdown = ctk.CTkOptionMenu(self.profile_tab, values=["Default"], command=lambda selection: self.switch_button.configure(state="disabled" if selection==self.current_profile_name else "normal"))
        self.profile_dropdown.grid(row=1, column=0, pady=(10, 10), padx=(10, 5), sticky="e")
        self.switch_button = ctk.CTkButton(self.profile_tab, text="Switch profile", font=TEXT_FONT, command=lambda: self.handle_switch_profile(self.profile_dropdown.get()))
        self.switch_button.grid(row=1, column=1, pady=(10, 10), padx=(5, 10), sticky="w")
        self.history_button = ctk.CTkButton(self.profile_tab, text="Generate viewing report", font=TEXT_FONT, command=self.open_history_callback)
        self.history_button.grid(row=2, column=0, columnspan=2, pady=(10, 10))
        self.subscription_tab = self.tabs.tab("Subscription")
        self.subscription_tab.grid_columnconfigure(0, weight=1)
        self.subscription_tab.grid_rowconfigure((0, 1), weight=1)
        self.upgrade_button = ctk.CTkButton(self.subscription_tab, text="Upgrade subscription", font=TITLE_FONT, command=self.upgrade_callback, fg_color=PRIMARY_COLOUR, hover_color=SECONDARY_COLOUR, text_color="white")
        self.upgrade_button.grid(row=1, column=0, pady=(10, 10), sticky="ew", padx=(10, 10))
        if self.account:
            self.sub_info = ctk.CTkLabel(self.subscription_tab, text=f"Current Plan: {self.account.subscription_plan.value}", font=TITLE_FONT)
        else:
            self.sub_info = ctk.CTkLabel(self.subscription_tab, text=f"Current Plan: None", font=TITLE_FONT)
        self.sub_info.grid(row=0, column=0, pady=(10, 10), sticky="ew", padx=(10, 10))

    def set_account(self, account):
        self.account = account
        self.sub_info.configure(text=f"Current Plan: {self.account.subscription_plan.value}")

    def handle_switch_profile(self, selection):
        if self.switch_profile_callback:
            self.switch_profile_callback(selection)

    def handle_upgrade(self, selection):
        if self.upgrade_callback:
            self.upgrade_callback(selection)

    def change_name(self, new_name):
        self.name = new_name
        self.title_label.configure(text=f"Account: {self.name}")

    def refresh_view(self, account, current_profile):
        self.title_label.configure(text=f"Profile: {current_profile.name}")
        self.current_profile_name = current_profile.name
        
        names = [p.name for p in account.profiles]
        self.profile_dropdown.configure(values=names)
        self.profile_dropdown.set(current_profile.name)
        self.switch_button.configure(state="disabled")

        if current_profile.is_adult:
            self.sub_info.configure(text=f"Plan: {account.subscription_plan.value} (Adult)")
            self.upgrade_button.grid(row=1, column=0)
        else:
            self.sub_info.configure(text=f"Plan: {account.subscription_plan.value} (Child)\nUpgrading blocked")
            self.upgrade_button.grid_forget()

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

        self.current_account_data = None
        self.current_profile = None

        self.home_frame = HomeFrame(self, self.name, self.watch_media)
        self.search_frame = SearchFrame(self, self.watch_media)
        self.star_frame = StarredFrame(self, self.watch_media)
        self.settings_frame = SettingsFrame(self)
        self.account_frame = AccountFrame(self, self.name, account=None, open_history_callback=self.show_history_window, upgrade_callback=self.upgrade_prompt, switch_profile_callback=self.handle_profile_switch)
        self.watch_frame = WatchFrame(self, Movie({}), self.toggle_favourite)

        self.current_frame = self.home_frame

        self.build_ui()

    def upgrade_prompt(self):
        if not self.current_account_data:
            return
        
        current_plan = self.current_account_data.subscription_plan.value
        if(current_plan == "PremiumPlan"):
            print("Account is already at highest tier.")
            return
        
        current_payment = self.current_account_data.get_payment_info()
        
        dialog = PaymentDialog(self, current_plan, lambda x: self.execute_upgrade(x), payment_info=current_payment)

    def execute_upgrade(self, target_plan: str):
        if not self.current_account_data:
            return
        
        if target_plan == "StandardPlan":
            self.current_account_data.subscription_plan = SubscriptionPlan.STANDARD
        elif target_plan == "PremiumPlan":
            self.current_account_data.subscription_plan = SubscriptionPlan.PREMIUM
        
        print(f"Successfully upgraded to {target_plan}")
        self.account_frame.set_account(self.current_account_data)

        try: # FIXME: weird idk if it saves data properly
            accounts_list = self.master.account_manager.load_accounts() # type: ignore
            for acc in accounts_list:
                if acc.username == self.current_account_data.username:
                    acc.subscription_plan = self.current_account_data.subscription_plan
                    break
            self.master.account_manager.update_accounts(accounts_list) # type: ignore
        except Exception as e:
            print(e)

        self.update_profile_ui()

    def handle_profile_switch(self, new_profile_name):
        if self.current_account_data:
            for p in self.current_account_data.profiles: # type: ignore FIXME:
                if p.name == new_profile_name:
                    self.current_profile = p
                    print(f"Switched profile to: {p.name} (Adult: {p.is_adult})")
                    self.change_name(p.name)
            self.update_profile_ui()

    def handle_upgrade(self, new_plan_str):
        if self.current_account_data:
            if new_plan_str == "Standard Plan":
                self.current_account_data.subscription_plan = SubscriptionPlan.STANDARD
            elif new_plan_str == "Premium Plan":
                self.current_account_data.subscription_plan = SubscriptionPlan.PREMIUM

        app = self.master
        app.account_manager.update_accounts(app.account_manager.load_accounts())
        self.update_profile_ui()

    def update_profile_ui(self):
        if self.current_account_data and self.current_profile:
            self.search_frame.current_account = self.current_account_data
            self.search_frame.current_profile = self.current_profile
            self.search_frame.refresh_content()
            self.account_frame.refresh_view(self.current_account_data, self.current_profile)
            self.home_frame.refresh_content(account=self.current_account_data, current_profile=self.current_profile)

    def show_history_window(self):
        history_list = []
        if self.current_account_data and self.current_account_data.profiles:
            history_list = self.current_account_data.profiles[0].watch_history

        history_window = WatchHistory(self, self.name, history_list, viewing_txt_path)
        history_window.focus()
    
    def build_ui(self):
        self.logo = ctk.CTkImage(images["small_logo"].resize((100, 100), resample=Image.Resampling.LANCZOS), size=(100,100))
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
        self.name = new_name
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
        self.loading_frame = LoadingFrame(self, loading_text="Loading...")
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
            password = logged_in_user.get_password()
            print(f"Logging in as {username} with password {password}")

            self.browse_frame.current_account_data = logged_in_user
            if logged_in_user.profiles:
                self.browse_frame.current_profile = logged_in_user.profiles[0]
            self.browse_frame.account_frame.set_account(logged_in_user)
            self.login_switch(username)
            return True
        else:
            return False

    def login_switch(self, user):
        self.switch_frame(self.login_frame, self.loading_frame)
        self.user = user
        self.browse_frame.change_name(user)
        self.browse_frame.update_profile_ui()
        self.after(500, lambda:self.switch_frame(self.loading_frame, self.browse_frame))

    def quit(self):
        self.destroy()

if __name__ == "__main__":
    app = StreamingApp()
    app.mainloop()