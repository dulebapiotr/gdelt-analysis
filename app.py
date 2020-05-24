from flask import Flask, render_template
import pandas as pd
import numpy as np
import gdelt
import script as scripts
from flask_cors import CORS

app = Flask(__name__)

gd1 = gdelt.gdelt(version=1)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods=['GET'])
def hello():
    x = scripts.events_between_countries("POL", "FRA", ['2020-05-07', '2020-05-08'])
    return render_template("analysis.html", name="events_between_countries", data=x)


if __name__ == '__main__':
    app.run()


