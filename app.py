import config
import requests
from flask import Flask, render_template
from flask import request, redirect

app = Flask(__name__)
# env_config = os.getenv("APP_SETTINGS", "config.DevelopmentConfig")
# app.config.from_object(env_config)

@app.route("/genre", methods=['POST', 'GET'])
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




    


