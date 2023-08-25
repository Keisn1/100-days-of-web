import requests
from program import app
from flask import render_template
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

