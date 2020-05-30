import pandas as pd


def insert_dataframe(input_data: pd.DataFrame):
    file = open("data.csv", "w", encoding="utf-8")
    csv_out = input_data.to_csv(index=False)
    file.write(csv_out)
    file.close()


def get_dataframe(start_date: int, stop_date: int):
    try:
        input_data = open("data.csv", "r", encoding="utf-8").read()
        df = pd.read_csv(input_data)
        select = df.loc[df['DATEADDED'].isin(range(start_date, stop_date + 1))]
        return select
    except FileNotFoundError:
        return pd.DataFrame()
