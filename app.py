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
    start = data.get('start')[
            0:10]  # possible the dumbest way to format a date, but whatevah. Normally it would be '2020-05-25 06:04:30,773' so i cut it short
    stop = data.get('stop')[0:10]
    if start == stop:
        date = start
    else:
        date = [start, stop]
    data = gd1.Search(date, table='events', output='pd')
    return data.to_json()

@app.route('/actors-action-geo', methods=['GET'])
def actors_action_geo():
    data = request.get_json()
    start = data.get('start')[0:10]  # possible the dumbest way to format a date, but whatevah. Normally it would be '2020-05-25 06:04:30,773' so i cut it short
    stop = data.get('stop')[0:10]
    actor1 = data.get('actor1')
    actor2 = data.get('actor2')
    if start == stop:
        date = start
    else:
        date = [start, stop]
    data = gd1.Search(date, table='events', output='pd')
    result = scripts.actors_action_geo(data, actor1, actor2)
    return result.to_json()


if __name__ == '__main__':
    app.run()
