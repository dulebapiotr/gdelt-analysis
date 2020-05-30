import pandas as pd

class DatabaseCsv(object):



    @staticmethod
    def insertDataframe(input_data: pd.DataFrame):
       file = open("data.csv", "w")
       csv_out = input_data.to_csv(index=False)
       file.write(csv_out)
       file.close()


    @staticmethod
    def getDataframe(startDate: int, stopDate: int):
        input_data = open("data.csv", "r").read()
        df = pd.read_csv(input_data)
        select = df.loc[df['DATEADDED'].isin(range(stopDate, stopDate+1))]
        return select



