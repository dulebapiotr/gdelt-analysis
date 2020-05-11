import gdelt
import pandas as pd
# Version 1 queries
gd1 = gdelt.gdelt(version=1)
results= gd1.Search('2020-05-10',table='events',output='pd') # to już jest DataFrame


#zwraca liczbe rodzajów wydarzeń w danym datasecie, biorę pod uwagę 2 pierwsze cyfry kodu CAMEO
def count_events(data, event_type):
    if not 1<=event_type<=20:
        return 0
    events = data[['EventCode']]
    #tutaj zawężam, bo kategorie są jeszcze bardziej uszczegółowione, interesują mnie tylko pierwsze 2 cyfry kodu CAMEO
    filtered = events.apply(lambda x:  int(x['EventCode'][:2]) , axis=1) 
    checked = filtered.apply(lambda x: 1 if x == event_type else 0 )
    return checked.sum()
#print(count_events(results,7))


# zwraca datafame z ilościa i % występowania poszczególnych typów zdarzeń w danym datasecie
def event_types_ratio(data):
    sum = data.shape[0] # no bo tyle jest wszystkich zdarzeń co rekordów
    dictionary = {"event_type_cameo": [], "count": [], "ratio": []}
    for x in range (1,21):
        count = count_events(data, x)
        dictionary["event_type_cameo"].append(x)
        dictionary["count"].append(count)
        dictionary["ratio"].append(count/sum)
    result = pd.DataFrame(data=dictionary)
    result.set_index('event_type_cameo')
    return result
#print(event_types_ratio(results))


# zwraca dataframe z współrzędnymi geograficznymi wydarzeń zachocących pomiędzy daną parą aktorów (podajemy ich kody CAMEO)
def actors_action_geo(data, cameo_1, cameo_2):
    results = data[["Actor1Code","Actor2Code","ActionGeo_Lat","ActionGeo_Long"]]
    filter1 = results["Actor1Code"]==cameo_1
    filter2 = results["Actor2Code"]==cameo_2
    
    return results[filter1 & filter2]
# print(actors_action_geo(results,"scoGOV",'GBR' ))

# punkt 4 analiz ilościowych - dla wybranego kraju, który jest jako Actor1, wylicza średnią miarę Goldsteina z krajami które są jako Actor2
def avg_goldstein_with_other_countries(dataframe, cameo1):
    data = dataframe[["Actor1Code","Actor2Code","AvgTone"]]
    dictionary={}

    for index, row in data.iterrows():
        if not row["Actor2Code"] in dictionary:
            dictionary[row["Actor2Code"]] = (row["AvgTone"],1)
        else:
            num = dictionary[row["Actor2Code"]][1]
            avg=  dictionary[row["Actor2Code"]][0]
            new_value = row["AvgTone"]
            dictionary[row["Actor2Code"]] = ((avg*num+new_value)/(num+1), num+1)
    result = pd.DataFrame(data=dictionary).T
    result.columns=[ "avg_goldstein", "events_count"]
    return result
#print(avg_goldstein_with_other_countries(results, "GBR"))

#punkt 5 analiz ilościowych - dla danej kolumny(jej nazwy) pokazuje jej wartości w czasie (uporządkowanym), nie wiem czy o to tutaj chodzi XD
def value_in_time(data, value):
    result = data[[value, "SQLDATE"]]
    result.sort_values(by=["SQLDATE"])
    return result
#print(value_in_time(results, "AvgTone"))


def events_between_countries(cameo_1, cameo_2, date):
    df = gd1.Search(date,table='events',output='pd')
    df = df.loc[(df['Actor1Code'] == cameo_1) & (df['Actor2Code'] == cameo_2)]
    return df

def count_events_between_countries(cameo_1, cameo_2, date):
    events = events_between_countries(cameo_1, cameo_2, date)
    return len(events.index)

def search_biggest_impact_on_countries(cameo_1, cameo_2, date):
    df = events_between_countries(cameo_1, cameo_2, date)
    df = df.loc[(df['AvgTone'] >= 10) | (df['AvgTone'] <= -10)]
    print(df)
search_biggest_impact_on_countries('USA', 'RUS', '2001-09-11')