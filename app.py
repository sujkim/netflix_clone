from re import A
from requests import api
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

apiBaseURL = 'https://api.themoviedb.org/3/'
fetchURL = apiBaseURL + 'discover/movie?api_key='
scriptURL = 'https://imsdb.com/scripts/'


@app.route("/search", methods=['GET'])
def search_movies(movies):
    """Given a list of movies, checks IMSDb for a script, and returns the movies"""
    movies_list = []
    scripts = []
    # only search first 10 results
    for movie in movies:
        title = movie['title']
        # prepare title for script site
        title_list = title.split()
        string = "-".join(title_list)
        # check if script is available, add available scipts
        page = requests.get(scriptURL + string + '.html')
        soup = BeautifulSoup(page.content, "html.parser")
        if soup.pre and soup.pre.text != '':
            movies_list.append(movie)
            scripts.append(string)
    return movies_list, scripts


@ app.route("/main", methods=['GET'])
def main():
    query_string_genres = apiBaseURL + 'genre/movie/list?api_key=' + config.api_key
    response = requests.get(query_string_genres)

    genres_results = response.json()['genres']

    params = {
        "sort_by": "popularity.desc",
        "include_adult": "false",
        "include_video": "false",
        "page": 1,
        "with_watch_providers": 8,
        "watch_region": "US",
        "with_original_language": "en"
        # "year": 1995
    }

    query_string = fetchURL + config.api_key

    collection = {}
    # for each genre, get list of popular movies
    for genre in genres_results:
        params['with_genres'] = str(genre['id'])

        fetch_movies = requests.get(query_string, params=params)
        movies_results = fetch_movies.json()['results']

        collection[genre['name']] = movies_results

    return render_template('main.html', collection=collection, imageURL="https://image.tmdb.org/t/p/w500")


@ app.route("/script/<title>", methods=['GET'])
def script(title):

    baseURL = "https://imsdb.com/scripts/"

    if request.method == 'GET':
        # prepare title for script site
        title_list = title.split()
        string = "-".join(title_list)

        # check if script is available, add available scipts
        page = requests.get(baseURL + string + '.html')
        soup = BeautifulSoup(page.content, "html.parser")
        script = soup.pre

        return script.text


@ app.route("/select/<string:id>", methods=['GET'])
def select_movie(id):

    if request.method == 'GET':
        query_string = apiBaseURL + 'movie/' + \
            str(id) + '?api_key=' + config.api_key

        response = requests.get(query_string)

        results = response.json()

        return results


@ app.route("/clips/<string:id>", methods=['GET'])
def clips(id):
    """Return Youtube key to display trailer"""

    fetch_videos = requests.get(
        apiBaseURL + 'movie/' + id + '/videos?' + 'api_key=' + config.api_key)

    videos = fetch_videos.json()['results']

    for video in videos:
        if video['type'] == 'Trailer':
            return video['key']
        else:
            return ''


@ app.route("/search", methods=['GET', 'POST'])
def search():

    if request.method == 'GET':

        return render_template('search.html')

    if request.method == 'POST':
        query_string = 'search/movie?api_key=' + \
            config.api_key + languageURL + 'query='

        movie_query = request.form.get('movie')

        # encode url
        encoded_string = urllib.parse.quote(movie_query)

        # send API request
        response = requests.get(
            apiBaseURL + query_string + encoded_string + endURL)

        results = response.json()['results']

        movies = []
        scripts = []

        # only search first 10 results
        for result in results[0:10]:
            title = result['title']

            # prepare title for script site
            title_list = title.split()
            string = "-".join(title_list)

            # check if script is available, add available scipts
            page = requests.get(scriptURL + string + '.html')
            soup = BeautifulSoup(page.content, "html.parser")
            if soup.pre.text != '':
                movies.append(result)
                scripts.append(string)

        # print(results)

        # build poster image
        imageURL = 'https://image.tmdb.org/t/p/w500'
        # imageURL = 'https://image.tmdb.org/t/p/w500/kEP1iw6GVqdS225dyyZelIYNo4S.jpg'

        return render_template('results.html', movies=movies, imageURL=imageURL, scripts=scripts)


# @ app.route("/genre", methods=['GET', 'POST'])
# def genre():
#     # secret_key = app.config.get("SECRET_KEY")
#     # return f"The configured secret key is {secret_key}."
#     # return "This is yet another new version!"

#     if request.method == 'GET':

#         # send request for list of genres
#         response = requests.get(
#             'https://api.themoviedb.org/3/genre/movie/list?api_key=' + config.api_key)
#         genres = response.json()['genres']

#         return render_template('genres.html', genres=genres)

#     if request.method == 'POST':

#         # user inputs
#         selections = request.form.getlist('genre')
#         # print(selections)

#         return redirect('/decade')


# @ app.route("/decade", methods=['POST', 'GET'])
# def decade():
#     # secret_key = app.config.get("SECRET_KEY")
#     # return f"The configured secret key is {secret_key}."
#     # return "This is yet another new version!"

#     if request.method == 'GET':

#         # send request for list of decades
#         response = requests.get(
#             'https://api.themoviedb.org/3/genre/movie/list?api_key=' + config.api_key)
#         genres = response.json()['genres']

#         return render_template('decades.html')

#     if request.method == 'POST':

#         # user inputs
#         selections = request.form.get('decade')
#         # print(selections)

#         return redirect('actors.html')
