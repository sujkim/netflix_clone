from re import A
from requests import api
import random
import config
import requests
import urllib.parse
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask import request, redirect
import json

app = Flask(__name__)
# env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
# app.config.from_object(env_config)

apiBaseURL = "https://api.themoviedb.org/3/"
fetchMoviesURL = apiBaseURL + "discover/movie?api_key="
fetchTVURL = apiBaseURL + "discover/tv?api_key="
scriptURL = "https://imsdb.com/scripts/"
imageURL = "https://image.tmdb.org/t/p/"


def get_trending():
    query_string = apiBaseURL + "/trending/movie/day?api_key=" + config.api_key
    details = requests.get(query_string)

    trending = details.json()["results"]

    return trending


def get_banner():

    banner = {}
    trailer = ""

    # verify there is a trailer available
    while trailer == "":
        movie = random.choice(get_trending())
        trailer = clips("movie", str(movie["id"]))

    banner["trailer"] = trailer
    # truncate description to 150 characters
    banner["overview"] = movie["overview"]
    banner["title"] = movie["title"]

    return banner


def get_media(type):

    fetchURL = fetchMoviesURL if type == "movies" else fetchTVURL

    query_string = fetchURL + config.api_key

    collection = {}

    params = {
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "include_video": "false",
        "page": 1,
        # "with_watch_providers": 8,
        "watch_region": "US",
        "with_original_language": "en"
        # "year": 1995
    }
    # for each genre, get list of popular movies/shows
    for genre in get_genres():
        params["with_genres"] = str(genre["id"])

        fetch_media = requests.get(query_string, params=params)

        results = fetch_media.json()["results"]

        if results:
            collection[genre["name"]] = results

    return collection


@ app.route("/", methods=["GET"])
def main():

    return render_template("index.html",
                           tv_collection=get_media("shows"),
                           movie_collection=get_media("movies"), banner=get_banner(),
                           imageURL=imageURL, trending=get_trending())


@ app.route("/shows", methods=["GET"])
def shows():

    return render_template("shows.html", collection=get_media("shows"), imageURL=imageURL)


@ app.route("/movies", methods=["GET"])
def movies():

    return render_template("movies.html", collection=get_media("movies"), imageURL=imageURL)


@ app.route("/script/<title>", methods=["GET"])
def script(title):

    baseURL = "https://imsdb.com/scripts/"

    if request.method == "GET":
        # prepare title for script site
        title_list = title.split()
        string = "-".join(title_list)

        # check if script is available, add available scipts
        page = requests.get(baseURL + string + ".html")

        if page.status_code == requests.codes.ok:
            soup = BeautifulSoup(page.content, "html.parser")
            script = soup.pre
            return script.text

        return ""


@ app.route("/select/<string:media_type>/<string:id>", methods=["GET"])
def select(media_type, id):
    query_string = apiBaseURL + media_type + "/" + \
        str(id) + "?api_key=" + config.api_key

    fetch_details = requests.get(query_string)
    response = fetch_details.json()

    details = {}

    details["year"] = response["release_date"][0:
                                               4] if media_type == "movie" else response["first_air_date"][0:4]
    details["runtime"] = response["runtime"] if media_type == "movie" else ""

    details["rating"] = str(response["vote_average"]) + "/10"
    details["overview"] = response["overview"]

    details["genres"] = [genre["name"] for genre in response["genres"]]
    details["cast"] = get_cast(media_type, id)

    return details


def get_cast(media_type, id):
    query_string = apiBaseURL + media_type + "/" + \
        str(id) + "/credits" + "?api_key=" + config.api_key

    fetch_credits = requests.get(query_string)

    credits = fetch_credits.json()["cast"]

    return [actor["name"] for actor in credits[0:6]]


@ app.route("/clips/<string:media_type>/<string:id>", methods=["GET"])
def clips(media_type, id):
    """Return Youtube key to display trailer"""

    fetch_videos = requests.get(
        apiBaseURL + media_type + "/" + id + "/videos?" + "api_key=" + config.api_key)

    videos = fetch_videos.json()["results"]

    for video in videos:
        if video["type"] == "Trailer" and video["official"] == True:
            # print(video)
            return video["key"]

    return ""


@ app.route("/search", methods=["GET", "POST"])
def search_movie():

    if request.method == "GET":

        return render_template("base.html")

    if request.method == "POST":

        search_input = request.form.get("search_input")

        results = search(search_input)

        return render_template("results.html", results=results, imageURL=imageURL, input=search_input)


def search(search_input):
    query_string = apiBaseURL + "search/movie?api_key=" + config.api_key

    params = {
        "language": "en-US",
        "query": search_input,
        "page": 1,
        "include_adult": "false"
    }

    fetch_movies = requests.get(query_string, params=params)
    # print(fetch_movies.url)

    movies = fetch_movies.json()["results"]

    query_string = apiBaseURL + "search/tv?api_key=" + config.api_key

    fetch_shows = requests.get(query_string, params=params)
    shows = fetch_shows.json()["results"]

    results = movies + shows

    return results


def get_genres():
    query_string_genres = apiBaseURL + "genre/movie/list?api_key=" + config.api_key
    details = requests.get(query_string_genres)

    genres = details.json()["genres"]

    return genres
