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


# Movie data analysis


movie_data = read(paths["movie"])

print(len(movie_data))
print(movie_data[0])

over_8_vote_avg_movies = [x for x in movie_data if x.get("vote_average",0)>=8]

print(len(over_8_vote_avg_movies))
print(over_8_vote_avg_movies[0])

us_movies = [x for x in movie_data if "US" in x.get("origin_country",[])]

print(len(us_movies))
print(us_movies[0])

non_us_movies = [x for x in movie_data if "US" not in x.get("origin_country",[])]

print(len(non_us_movies))
print(non_us_movies[0])

sorted_by_size = sorted(movie_data, key=lambda x:x.get("runtime",float("inf")))

print(sorted_by_size[0])
print(sorted_by_size[-1])

