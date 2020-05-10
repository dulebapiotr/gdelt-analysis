from flask import Flask, render_template
import pandas as pd
import numpy as np
import gdelt
app = Flask(__name__)

gd1 = gdelt.gdelt(version=1)

def events_between_countries(cameo_1, cameo_2, date):
    df = gd1.Search(date,table='events',output='pd')
    df = df.loc[(df['Actor1Code'] == cameo_1) & (df['Actor2Code'] == cameo_2)]
    return df

@app.route('/')
def hello():
    x = events_between_countries("POL", "FRA", ['2020-05-07', '2020-05-08'])
    return render_template("analysis.html", name="wow", data=x)



if __name__ == '__main__':
    app.run()


