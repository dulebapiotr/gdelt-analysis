from time import strptime, strftime

from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import gdelt
import script as scripts
from flask_cors import CORS
import gdelt
import datetime
import analysis_manager
from Session import Session
import json
import database_csv as db

app = Flask(__name__)

gd1 = gdelt.gdelt(version=1)
session: Session = Session()
CORS(app, resources={r'/*': {'origins': '*'}})


def get_gdelt_data(start: str, stop: str) -> pd.DataFrame:
    res_df = pd.DataFrame()
    start_time = strptime(start, "%Y-%m-%d")
    stop_time = strptime(stop, "%Y-%m-%d")
    date_start = int(strftime('%Y%m%d', start_time))
    date_stop = int(strftime('%Y%m%d', stop_time))
    for i in range(date_start, date_stop + 1):
        df = db.get_dataframe(i, i)
        if df.shape[0] >= 1:
            pd.concat([res_df, df])
        else:
            df = gd1.Search(str(i), table='events', output='pd')
            db.insert_dataframe(df)
            res_df = pd.concat([res_df, df])

    return res_df


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
        res.append((val, longg[x]))
    print(res)
    print(json.dumps(res))
    return json.dumps(res)


# stworzenie nowej sesji (zakres czasu)
@app.route('/new_session', methods=['POST'])
def new_session():
    data = request.get_json()
    start = data.get('start')[0:10]
    stop = data.get('stop')[0:10]
    if start == stop:
        df = get_gdelt_data(start, start)
    else:
        df = get_gdelt_data(start, stop)
    global session
    session = Session()
    session.add_data(df, "raw_result")
    return "succesfully got data"  # to stanowczo za duże żeby przesłać jsonem


# pobranie danych z sesji (void) - chyba jednak nie jkest void xD
@app.route('/get_session', methods=["GET"])
def get_session():
    global session
    return jsonify(session.get_all_data())


@app.route('/get_analysis', methods=["GET"])
def get_analysis():
    global session
    data = request.get_json()
    name = data.get('name')
    return session.get_data(name).to_json()


@app.route('/add_analysis', methods=["POST"])
def add_analysis():
    data = request.get_json()
    analysis_name = data.get('analysis_name')
    df_name = data.get('df_name')
    params = data.get('params')
    print(type(params))
    print(params)
    result_name, result = analysis_manager.add_analysis(session, df_name, analysis_name, params)
    if isinstance(result, pd.DataFrame):
        return result.to_json(orient="records")
    else:
        return jsonify(result)


if __name__ == '__main__':
    app.run()
