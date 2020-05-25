from flask import Flask, request
import pandas as pd
import numpy as np
import gdelt
import script as scripts
from flask_cors import CORS
import gdelt
import datetime

app = Flask(__name__)

gd1 = gdelt.gdelt(version=1)

CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/dataframes', methods=['POST'])
def dataframe():
    data = request.get_json()
    start = data.get('start')[0:10]  # really a stupid way to format date
    stop = data.get('stop')[0:10]
    if start == stop:
        date = start
    else:
        date = [start, stop]
    data = gd1.Search(date, table='events', output='pd')
    return data.to_json()


if __name__ == '__main__':
    app.run()


