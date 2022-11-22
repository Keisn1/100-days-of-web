from program import app
from flask import render_template

@app.route('/')                 # root- or index- path
@app.route('/index')            # "What is the decorator run against?"
def index():                # try and name functions similar to url, route-name
    return render_template('index.html')

@app.route('/100Days')
def p100Days():
    return render_template('100Days.html')

