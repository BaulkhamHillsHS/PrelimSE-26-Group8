from pathlib import Path
import os,json
def read(path):
    with open(path, "r") as f:
        return json.load(f)
def write(path, data):
    with open(path, "w") as f:
        json.dump(data, f)
root = Path(__file__).resolve().parent
paths = {}
for datafile in ["anime_movies", "anime", "movie", "tv"]:
    paths[datafile] = os.path.join(root, datafile + ".json")


# class structures


class Movie:
    def __init__(self, data):
        self.adult = data.get("adult", False)
        self.backdrop_path = data.get("backdrop_path","")
        self.belongs_to_collection = data.get("belongs_to_collection", {})
        self.budget = data.get("budget", 0)
        self.genres = data.get("genres", [])
        self.id = data.get("id", 0)
        self.imdb_id = data.get("imdb_id", 0)
        self.origin_country = data.get("origin_country", [])
        self.overview = data.get("overview", "")
        self.popularity = data.get("popularity", 0.0)
        self.poster_path = data.get("poster_path", "")
        self.release_date = data.get("release_date", "")
        self.spoken_languages = data.get("spoken_languages", "")
        self.runtime = data.get("runtime", 0)
        self.title = data.get("title", "")
        self.vote_average = data.get("vote_average", 0.0)
    def __str__(self):
        return f"{self.title}({self.release_date}) - {self.runtime//60}h{self.runtime%60}m from {self.origin_country}, genres ({', '.join([x.get('name') for x in self.genres])})"
    def get_runtime(self):
        return self.runtime
    def get_image_url(self):
        return "https://image.tmdb.org/t/p/w500" + self.poster_path

movie_data = read(paths["movie"])

import random
random_movie = random.choice(movie_data)
mymovie = Movie(random_movie)

print(mymovie)
print(mymovie.get_image_url())

from PIL import Image
import requests
from io import BytesIO

response = requests.get(mymovie.get_image_url())
img = Image.open(BytesIO(response.content))
img.show()