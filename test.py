from typing import Dict

import gdelt
import pandas as pd
import numpy as np
import database_csv as db



# gd1 = gdelt.gdelt(version=1)
# results1= gd1.Search('2020 May 28',table='events', output='pd')
# results2= gd1.Search('2020 May 29',table='events', output='pd')
# tmp1 = results1[["SQLDATE",'EventCode',"Actor1Code", "Actor2Code", "DATEADDED",  "AvgTone", "ActionGeo_Lat", "ActionGeo_Long"]]
# tmp2 = results2[["SQLDATE",'EventCode',"Actor1Code", "Actor2Code", "DATEADDED",  "AvgTone", "ActionGeo_Lat", "ActionGeo_Long"]]
# print("---------WRITE----------------")
# tmp = pd.concat([tmp1,tmp2])
# csv_out = tmp.to_csv(index=False)
# my_file = open("data.csv", "w")
# my_file.write(csv_out)
# my_file.close()

# print("--------READ--------------")
# input_data = open("data.csv", "r").read()
# single_df = pd.read_csv(input_data)
# print(single_df)


gd1 = gdelt.gdelt(version=1)
results1= gd1.Search('20200513',table='events', output='pd')
# results2= gd1.Search('20200529',table='events', output='pd')
tmp1 = results1[["SQLDATE",'EventCode',"Actor1Code", "Actor2Code", "DATEADDED",  "AvgTone", "ActionGeo_Lat", "ActionGeo_Long"]]
# tmp2 = results2[["SQLDATE",'EventCode',"Actor1Code", "Actor2Code", "DATEADDED",  "AvgTone", "ActionGeo_Lat", "ActionGeo_Long"]]

print(tmp1)