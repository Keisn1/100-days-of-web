from quart import Quart

app = Quart(__name__)

from program import routes
