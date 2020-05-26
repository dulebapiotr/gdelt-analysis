from flask import Flask, request
import pandas as pd
import numpy as np
import gdelt
import script as scripts
from flask_cors import CORS
import gdelt
import datetime
import analysis_manager 
import Session
import json
app = Flask(__name__)

gd1 = gdelt.gdelt(version=1)
session = Session.Session('2020-05-24')
CORS(app, resources={r'/*': {'origins': '*'}})

#dodanie danych do analizy (zapytanie do gdelta)
@app.route('/dataframes', methods=['POST'])
def dataframe():
    data = request.get_json()
    start = data.get('start')[0:10]  # possible the dumbest way to format a date, but whatevah. Normally it would be '2020-05-25 06:04:30,773' so i cut it short
    stop = data.get('stop')[0:10]
    if start == stop:
        date = start
    else:
        date = [start, stop]
    data = gd1.Search(date, table='events', output='pd')
    return data.to_json()

@app.route('/actors-action-geo', methods=['POST'])
def actors_action_geo():
    data = request.get_json()
    print(request.get_json())
    start = data.get('start')[0:10]
    stop = data.get('stop')[0:10]
    actor1 = data.get('actor1')
    actor2 = data.get('actor2')
    if start == stop:
        date = start
    else:
        date = [start, stop]
    data = gd1.Search(date, table='events', output='pd')
    result = scripts.actors_action_geo(data, actor1, actor2)
    print(result)
    lat = result["ActionGeo_Lat"]
    longg = result["ActionGeo_Long"]
    res = []
    for x, val in lat.items():
        print(val)
        res.append((val,longg[x]))
    print(res)
    print(json.dumps(res))
    return json.dumps(res)


# stworzenie nowej sesji (zakres czasu)
@app.route('/new_session', methods=['POST'])
def new_session():
    data = request.get_json()
    start = data.get('start')[0:10] 
    stop = data.get('stop')[0:10]
    time_range = [start, stop]
    if start == stop:
        date = start
    df = gd1.Search(time_range, table='events', output='pd')
    global session 
    session = Session.Session(time_range)
    session.add_data(df, "dataframe")
    return df.to_json()
#pobranie danych z sesji (void) - chyba jednak nie jkest void xD



@app.route('/get_session', methods=["POST"])
def get_session():
    data = request.get_json()
    name = data.get('name')
    return session.get_data(name).to_json


@app.route('/add_analysis', methods=["POST"])

def add_analysis():
    data = request.get_json()
    analysis_name = data.get('analysis_name')
    df_name = data.get('df_name')
    params = data.get('params')
    result_name, result_dataframe = analysis_manager.add_analysis(session, df_name, analysis_name, params)
    return tuple(result_name, result_dataframe)




if __name__ == '__main__':
    app.run()


