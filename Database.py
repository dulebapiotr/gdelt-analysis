import pymongo
import pandas as pd
import gridfs

class Database(object):
    URI = "mongodb://127.0.0.1:27017"
    client = pymongo.MongoClient(URI)
    DATABASE = client['gdeltDB']
    dataframes = DATABASE["dataframes"]
    cameos = DATABASE["cameos"]





    #split input dataframe by days(DATEADD column), and push it to database
    @staticmethod
    def insertDataframe(input_data: pd.DataFrame):
        #first we have to split out dataframe to pieces, each max 16MB.
        #i just cut it to 10k row pieces xD
        row_count = input_data.shape[0]
        for i in range(0,row_count,10000):
            ceil=0
            if i+10000>row_count:
                ceil=row_count
            else:
                ceil = i+10000
            chunk = input_data.truncate(before= i, after=ceil)
            #here we can insert chunk to database (it has less than 16MB)
            days_in_dataframe = chunk.DATEADDED.unique()
            for day in days_in_dataframe:
                #cut this part of input dataframe with specified event date
                df = chunk[input_data['DATEADDED']==day].to_json(orient='table')
                part = {"date": int(day), "data": df}
                Database.dataframes.insert_one(part)



        

    #return dataframe that contains all days from DB between startDate and intDate    
    # startDate and stopdate has format: yyyymmdd for example: 20200522   (int) 
    @staticmethod
    def getDataframe(startDate: int, stopDate: int):
        result_dataframe = pd.DataFrame()
        query = {"date": {"$gte":startDate, "$lte": stopDate}}
        results = Database.dataframes.find(query)
        for result in results:
            json_data = result["data"]
            single_df = pd.read_json(json_data, orient='table')
            result_dataframe = pd.concat([result_dataframe, single_df])

        return result_dataframe



        