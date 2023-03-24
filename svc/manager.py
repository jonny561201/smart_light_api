from flask import Flask

from svc.routes.light_routes import LIGHT_BLUEPRINT


app = Flask(__name__)
app.register_blueprint(LIGHT_BLUEPRINT)

