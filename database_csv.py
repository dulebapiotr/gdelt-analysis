import pandas as pd


def insert_dataframe(input_data: pd.DataFrame):
    file = open("data.csv", "w")
    csv_out = input_data.to_csv(index=False)
    file.write(csv_out)
    file.close()


def get_dataframe(start_date: int, stop_date: int):
    input_data = open("data.csv", "r").read()
    df = pd.read_csv(input_data)
    select = df.loc[df['DATEADDED'].isin(range(start_date, stop_date + 1))]
    return select
