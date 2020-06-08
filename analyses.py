from typing import Dict
import json
import gdelt
import pandas as pd
import numpy as np


# TODO: split into separate files

# Graphable analyses
# Deprecated
def count_events(data: pd.DataFrame, args: Dict):
    # TODO: Error handling when invalid args
    print(args)
    event_type = int(args["event_type"])
    if not 1 <= event_type <= 20:
        return 0
    events = data[['EventCode']]
    # tutaj zawężam, bo kategorie są jeszcze bardziej uszczegółowione, interesują mnie tylko pierwsze 2 cyfry kodu CAMEO
    filtered = events.apply(lambda x: int(x['EventCode'][:2]), axis=1)
    checked = filtered.apply(lambda x: 1 if x == event_type else 0)
    return int(checked.sum())


def filter_events_relation(data: pd.DataFrame, args: Dict):
    """
    sample args to find events of Goldstein Scale 0<=6 with at least 2 sources:
        {
            filters: [
                        {column_name: 'NumSources', relation: 'GT', reference: 2},
                        {column_name: 'GoldsteinScale', relation: 'GTE', reference: 0},
                        {column_name: 'GoldsteinScale', relation: 'LT', reference: 6}
                     ]
        }
    """
    days = data['SQLDATE'].unique()

    for filter_dict in args['filters']:

        column_name = filter_dict['column_name']
        relation = filter_dict['relation']
        reference = filter_dict['reference']

        if relation == 'GT':
            data = data.loc[data[column_name] > reference]
        elif relation == 'LT':
            data = data.loc[data[column_name] < reference]
        elif relation == 'GTE':
            data = data.loc[data[column_name] >= reference]
        elif relation == 'LTE':
            data = data.loc[data[column_name] <= reference]
        elif relation == 'EQ':
            data = data.loc[data[column_name] == reference]
        elif relation == 'NEQ':
            data = data.loc[data[column_name] != reference]

    return count_by_day(data, days)

def count_by_day(data: pd.DataFrame, days: pd.DataFrame = pd.DataFrame()):
    grouped = data[['SQLDATE', 'GLOBALEVENTID']]
    grouped = grouped.groupby('SQLDATE').count()
    grouped = grouped.rename(columns={'GLOBALEVENTID': 'EVENTCOUNT'})
    #TODO: add zero values for days with no data
    return grouped.sort_values(by='SQLDATE')

# Deprecated (also wrong)
# punkt 5 analiz ilościowych - dla danej kolumny(jej nazwy) pokazuje jej wartości w czasie (uporządkowanym),
# nie wiem czy o to tutaj chodzi XD
def value_in_time(data: pd.DataFrame, args: Dict):
    # TODO: Error handling when invalid args
    value = args['value']
    result = data[[value, "SQLDATE"]]
    result.sort_values(by=["SQLDATE"])
    return result


# tested!
def polynomial_fit(data: pd.DataFrame, args: Dict):
    # TODO: Error handling when invalid args
    column_name = args["column_name"]
    degree = int(args["degree"])
    if column_name not in data.columns:
        raise Exception
    vector = data[column_name]
    polyfit = np.polynomial.polynomial.Polynomial.fit(
        y=vector,
        x=range(0, len(vector)),
        deg=degree)

    return polyfit.coef.tolist()


# tested!
def get_mean_std_var(data: pd.DataFrame, args: Dict):
    # TODO: Error handling when invalid args
    column_name = args["column_name"]
    if column_name not in data.columns:
        raise Exception
    vector = data[column_name]
    return {"mean": vector.mean(),
            "std_dev": vector.std(),
            "variance": vector.var()}


# tested!
def get_median(data: pd.DataFrame, args: Dict):
    # TODO: Error handling when invalid args
    column_name = args["column_name"]
    if column_name not in data.columns:
        raise Exception
    return np.median(data[column_name])


# tested!
def get_range_ptp(data: pd.DataFrame, args: Dict):
    # TODO: Error handling when invalid args
    column_name = args["column_name"]
    if column_name not in data.columns:
        raise Exception
    vector = data[column_name]
    return {"min": int(np.amin(vector)),
            "max": int(np.amax(vector)),
            "ptp": int(np.ptp(vector))}


# tested!
def get_percentile(data: pd.DataFrame, args: Dict):
    # TODO: Error handling when invalid args
    column_name = args["column_name"]
    percentile = int(args["percentile"])
    if column_name not in data.columns:
        raise Exception
    elif not 0 <= percentile <= 100:
        raise Exception
    return np.percentile(data[column_name], percentile)


# zwraca datafame z ilościa i % występowania poszczególnych typów zdarzeń w danym datasecie
def event_types_ratio(data: pd.DataFrame, _):
    # no bo tyle jest wszystkich zdarzeń co rekordów
    event_count = data.shape[0]
    dictionary = {"event_type_cameo": [], "count": [], "ratio": []}
    for x in range(1, 21):
        count = count_events(data, {"event_type": x})
        dictionary["event_type_cameo"].append(x)
        dictionary["count"].append(count)
        dictionary["ratio"].append(count / event_count)
    result = pd.DataFrame(data=dictionary)
    result.set_index('event_type_cameo')
    return result


# Map-oriented analyses


def events_between_countries(data: pd.DataFrame, cameo_1, cameo_2):
    return data.loc[(data['Actor1Code'] == cameo_1) & (data['Actor2Code'] == cameo_2)]


def count_events_between_countries(data: pd.DataFrame, cameo_1, cameo_2):
    events = events_between_countries(data, cameo_1, cameo_2)
    return len(events.index)


def search_biggest_impact_on_countries(data: pd.DataFrame, cameo_1, cameo_2):
    df = events_between_countries(data, cameo_1, cameo_2)
    df = df.loc[(df['AvgTone'] >= 10) | (df['AvgTone'] <= -10)]
    return df


# TODO: Gaben fix pls | czemu tu się nie używa cameo1?
def avg_goldstein_with_other_countries(data: pd.DataFrame, cameo1):
    df_trim = data.loc[data['Actor1Code'] == cameo1]
    df = df_trim[["Actor1Code", "Actor2Code", "AvgTone"]]

    dictionary = {}

    for index, row in df.iterrows():
        if not row["Actor2Code"] in dictionary:
            dictionary[row["Actor2Code"]] = (row["AvgTone"], 1)
        else:
            num = dictionary[row["Actor2Code"]][1]
            avg = dictionary[row["Actor2Code"]][0]
            new_value = row["AvgTone"]
            dictionary[row["Actor2Code"]] = (
                (avg * num + new_value) / (num + 1), num + 1)
    result = pd.DataFrame(data=dictionary).T
    result.columns = ["avg_goldstein", "events_count"]
    return result


# zwraca dataframe z współrzędnymi geograficznymi wydarzeń zachocących pomiędzy daną parą aktorów (podajemy ich kody
# CAMEO)
def actors_action_geo(data: pd.DataFrame, cameo_1, cameo_2):
    results = data[["Actor1Code", "Actor2Code",
                    "ActionGeo_Lat", "ActionGeo_Long"]]
    filter1 = (results["Actor1Code"] == cameo_1) | (
        results["Actor2Code"] == cameo_1)
    filter2 = (results["Actor2Code"] == cameo_2) | (
        results["Actor1Code"] == cameo_2)
    return results[filter1 & filter2]


def actors_action_geo_json(data: pd.DataFrame, cameo_1, cameo_2):
    result1 = actors_action_geo(data, cameo_1, cameo_2)
    lat = result1["ActionGeo_Lat"]
    lon = result1["ActionGeo_Long"]
    res = {}
    for x, val in lat.items():
        inp = (val, lon[x])
        if inp in res:
            res[inp] += 1
        else:
            res[inp] = 1
    final_result = []
    for x, val in res.items():
        final_result.append((x[0], x[1], val))
    return final_result


if __name__ == "__main__":
    sample_data = pd.read_csv("data.csv")
    print(sample_data)
    print(count_by_day(sample_data))
    sample_args = json.loads("""{
                                    "filters": [
                                        {"column_name": "NumSources", "relation": "GT", "reference": 2},
                                        {"column_name": "GoldsteinScale", "relation": "GTE", "reference": 0},
                                        {"column_name": "GoldsteinScale", "relation": "LT", "reference": 6}
                                    ]
                                }
                                """
                             )
    print(filter_events_relation(sample_data, sample_args))
