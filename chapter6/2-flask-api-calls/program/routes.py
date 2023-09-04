import requests
from program import app
from flask import render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from datetime import datetime

timenow = str(datetime.today())



@app.route('/')                 # root- or index- path
@app.route('/index')            # "What is the decorator run against?"
def index():                # try and name functions similar to url, route-name
    return render_template('index.html', time=timenow)

@app.route('/100Days')
def p100Days():
    return render_template('100Days.html')

@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html', joke=joke)

def get_chuck_joke() -> str:
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data.get('value')



def get_poke_colours(colour) -> list:
    r = requests.get('https://pokeapi.co/api/v2/pokemon-color/' + colour.lower())
    if r.status_code == 404:
        return []
    pokedata = r.json()
    pokemon = []
    for p in pokedata['pokemon_species']:
        pokemon.append(p['name'])

    return pokemon

class ColourForm(FlaskForm):
    """
    To validate colour input from user
    """
    colour = StringField('colour', validators=[InputRequired(), Length(min=1, max=20)])

@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    form = ColourForm()
    if form.validate_on_submit():
        colour = form.colour.data
        pokemon = get_poke_colours(colour)
    return render_template('pokemon.html', pokemon=pokemon, form=form)

