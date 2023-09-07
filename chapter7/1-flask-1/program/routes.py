from program import app

from quart import render_template

@app.route('/')
@app.route('/index')
async def index():
    return await render_template('index.html')

@app.route('/100days')
async def p100days():
    return await render_template('100days.html')
