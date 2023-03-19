from flask import Flask

from svc.routes.lights import LIGHT_BLUEPRINT


app = Flask(__name__)
app.register_blueprint(LIGHT_BLUEPRINT)

