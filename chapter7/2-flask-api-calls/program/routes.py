import aiohttp
import aiohttp.client_exceptions
from program import app
from quart import render_template
from quart_wtf import QuartForm
from wtforms import StringField
from wtforms.validators import InputRequired, Length
from datetime import datetime

timenow = str(datetime.today())


@app.route('/')                 # root- or index- path
@app.route('/index')            # "What is the decorator run against?"
async def index():                # try and name functions similar to url, route-name
    return await render_template('index.html', time=timenow)

@app.route('/100Days')
async def p100Days():
    return await render_template('100Days.html')

@app.route('/chuck')
async def chuck():
    joke = await get_chuck_joke()
    return await render_template('chuck.html', joke=joke)

async def get_chuck_joke() -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://api.chucknorris.io/jokes/random') as response:
            response.raise_for_status()
            data = await response.json()
    return data.get('value')

async def get_poke_colours(colour) -> list:
    async with aiohttp.ClientSession() as session:
        async with session.get('https://pokeapi.co/api/v2/pokemon-color/' + colour.lower()) as response:
            try:
                response.raise_for_status()
                pokedata = await response.json()
            except aiohttp.client_exceptions.ClientResponseError as err:
                print(err)
                return []

    pokemon = []
    for p in pokedata['pokemon_species']:
        pokemon.append(p['name'])

    return pokemon

class ColourForm(QuartForm):
    """
    To validate colour input from user
    """
    colour = StringField('colour', validators=[InputRequired(), Length(min=1, max=20)])

@app.route('/pokemon', methods=['GET', 'POST'])
async def pokemon():
    pokemon = []
    form = await ColourForm().create_form()
    if await form.validate_on_submit():
        colour = form.colour.data
        pokemon = await get_poke_colours(colour)
    return await render_template('pokemon.html', pokemon=pokemon, form=form)
