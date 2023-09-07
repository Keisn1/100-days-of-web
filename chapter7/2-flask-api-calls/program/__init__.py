from quart import Quart

app = Quart(__name__)
app.config['SECRET_KEY'] = 'your secret key'
from program import routes
