from program import app

@app.route('/')                 # root- or index- path
@app.route('/index')            # "What is the decorator run against?"
def index():                # try and name functions similar to url, route-name
    return 'Hello Pyhonistas'
