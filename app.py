import config
import requests
import urllib
from bs4 import BeautifulSoup
from flask import Flask, render_template
from flask import request, redirect

app = Flask(__name__)
# env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
# app.config.from_object(env_config)

apiBaseURL = 'https://api.themoviedb.org/3/'
languageURL = '&language=en-US&'
endURL = '&page=1&include_adult=false'




@app.route("/", methods=['GET', 'POST'])
def main():
    baseURL = "https://imsdb.com/scripts/"

    # page = requests.get(URL)

    # soup = BeautifulSoup(page.content, "html.parser")
    # script = str(soup.find("pre"))
    # script = soup.pre
    # print(",".join(script))
    # print(lines)
    # print(script.find_all('b'))
    # for line in script.find_all('b'):
        # print(line.extract().text)

    print("whoo!")

    if request.method == 'GET':

    # print(script)
    # print(type(script))
    # print(script.get_text(separator='\n', strip=True))
    
    
        return render_template('main.html')

    if request.method == 'POST':
        query_string = 'search/movie?api_key=' + config.api_key + languageURL + 'query='



        movie_query = request.form.get('movie')

        # encode url
        encoded_string = urllib.parse.quote(movie_query)

        # send API request
        response = requests.get(apiBaseURL + query_string + encoded_string + endURL)

        # response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=658b17b3ab829a7b3494b7d40e9d5c26&language=en-US&query=MY%20GIRL&page=1&include_adult=false')

        results = response.json()['results']
        
        # print(results)

        # build poster image
        imageURL = 'https://image.tmdb.org/t/p/w500'
        # imageURL = 'https://image.tmdb.org/t/p/w500/kEP1iw6GVqdS225dyyZelIYNo4S.jpg'


        
        return render_template('results.html', results = results, imageURL = imageURL)

@app.route("/genre", methods=['GET', 'POST'])
def genre():
    # secret_key = app.config.get("SECRET_KEY")
    # return f"The configured secret key is {secret_key}."
    # return "This is yet another new version!"
    
    if request.method == 'GET':

        # send request for list of genres
        response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=' + config.api_key)
        genres = response.json()['genres']

        return render_template('genres.html', genres = genres)


    if request.method == 'POST':

        # user inputs
        selections = request.form.getlist('genre')
        print(selections)

        return redirect('/decade')


@app.route("/decade", methods=['POST', 'GET'])
def decade():
    # secret_key = app.config.get("SECRET_KEY")
    # return f"The configured secret key is {secret_key}."
    # return "This is yet another new version!"
    
    if request.method == 'GET':

        # send request for list of decades
        response = requests.get('https://api.themoviedb.org/3/genre/movie/list?api_key=' + config.api_key)
        genres = response.json()['genres']

        return render_template('decades.html')


    if request.method == 'POST':

        # user inputs
        selections = request.form.get('decade')
        print(selections)

        return redirect('actors.html')


@app.route("/runtime", methods=['POST', 'GET'])
def runtime():
    # secret_key = app.config.get("SECRET_KEY")
    # return f"The configured secret key is {secret_key}."
    # return "This is yet another new version!"
    
    if request.method == 'GET':


        return render_template('runtime.html')


    if request.method == 'POST':

        # user inputs
        selections = request.form.get('runtime')
        print(selections)

        return "success"




    


