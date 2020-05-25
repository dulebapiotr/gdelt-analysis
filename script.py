import gdelt
import pandas as pd
import numpy as np


# TODO: split into separate files

# Graphable analyses
# TODO: normalize APIs (parameters and return types)
# zwraca liczbe rodzajów wydarzeń w danym datasecie, biorę pod uwagę 2 pierwsze cyfry kodu CAMEO
def count_events(data, event_type):
    if not 1 <= event_type <= 20:
        return 0
    events = data[['EventCode']]
    # tutaj zawężam, bo kategorie są jeszcze bardziej uszczegółowione, interesują mnie tylko pierwsze 2 cyfry kodu CAMEO
    filtered = events.apply(lambda x: int(x['EventCode'][:2]), axis=1)
    checked = filtered.apply(lambda x: 1 if x == event_type else 0)
    return checked.sum()


# punkt 5 analiz ilościowych - dla danej kolumny(jej nazwy) pokazuje jej wartości w czasie (uporządkowanym),
# nie wiem czy o to tutaj chodzi XD
def value_in_time(data, value):
    result = data[[value, "SQLDATE"]]
    result.sort_values(by=["SQLDATE"])
    return result


def polynomial_fit(data, column_name, degree):
    if column_name not in data.columns:
        raise Exception
    vector = data[column_name]
    polynomial = np.polynomial.polynomial.Polynomial.fit(y=vector, x=range(0, len(vector)), deg=degree)
    return polynomial[0].convert().coef  # działało bez [0] ale pycharm krzyczał xD


def get_mean_std_var(data, column_name):
    if column_name not in data.columns:
        raise Exception
    vector = data[column_name]
    return {"mean": vector.mean(),
            "std_dev": vector.std(),
            "variance": vector.var()}


def get_median(data, column_name):
    if column_name not in data.columns:
        raise Exception
    return np.median(data[column_name])


def get_range_ptp(data, column_name):
    if column_name not in data.columns:
        raise Exception
    vector = data[column_name]
    return {"min": np.amin(vector),
            "max": np.amax(vector),
            "ptp": np.ptp(vector.var)}


def get_percentile(data, column_name, percentile):
    if column_name not in data.columns:
        raise Exception
    elif not 0 <= percentile <= 100:
        raise Exception
    return np.percentile(data[column_name], percentile)


# zwraca datafame z ilościa i % występowania poszczególnych typów zdarzeń w danym datasecie
def event_types_ratio(data):
    event_count = data.shape[0]  # no bo tyle jest wszystkich zdarzeń co rekordów
    dictionary = {"event_type_cameo": [], "count": [], "ratio": []}
    for x in range(1, 21):
        count = count_events(data, x)
        dictionary["event_type_cameo"].append(x)
        dictionary["count"].append(count)
        dictionary["ratio"].append(count / event_count)
    result = pd.DataFrame(data=dictionary)
    result.set_index('event_type_cameo')
    return result


# Map-oriented analyses


def events_between_countries(cameo_1, cameo_2, date):
    df = gd1.Search(date, table='events', output='pd')
    df = df.loc[(df['Actor1Code'] == cameo_1) & (df['Actor2Code'] == cameo_2)]
    return df


def count_events_between_countries(cameo_1, cameo_2, date):
    events = events_between_countries(cameo_1, cameo_2, date)
    return len(events.index)


def search_biggest_impact_on_countries(cameo_1, cameo_2, date):
    df = events_between_countries(cameo_1, cameo_2, date)
    df = df.loc[(df['AvgTone'] >= 10) | (df['AvgTone'] <= -10)]
    print(df)


def avg_goldstein_with_other_countries(dataframe, cameo1):
    data = dataframe[["Actor1Code", "Actor2Code", "AvgTone"]]
    dictionary = {}

    for index, row in data.iterrows():
        if not row["Actor2Code"] in dictionary:
            dictionary[row["Actor2Code"]] = (row["AvgTone"], 1)
        else:
            num = dictionary[row["Actor2Code"]][1]
            avg = dictionary[row["Actor2Code"]][0]
            new_value = row["AvgTone"]
            dictionary[row["Actor2Code"]] = ((avg * num + new_value) / (num + 1), num + 1)
    result = pd.DataFrame(data=dictionary).T
    result.columns = ["avg_goldstein", "events_count"]
    return result


# zwraca dataframe z współrzędnymi geograficznymi wydarzeń zachocących pomiędzy daną parą aktorów (podajemy ich kody
# CAMEO)
def actors_action_geo(data, cameo_1, cameo_2):
    results = data[["Actor1Code", "Actor2Code", "ActionGeo_Lat", "ActionGeo_Long"]]
    filter1 = results["Actor1Code"] == cameo_1 or results["Actor2Code"] == cameo_1
    filter2 = results["Actor2Code"] == cameo_2 or results["Actor1Code"] == cameo_2

    return results[filter1 & filter2]
