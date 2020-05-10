import gdelt
import pandas as pd
# Version 1 queries
gd1 = gdelt.gdelt(version=1)
results= gd1.Search('2020-05-08',table='events',output='pd') # to już jest DataFrame


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

def events_between_countries(cameo_1, cameo_2, date):
    df = gd1.Search(date,table='events',output='pd')
    df = df.loc[(df['Actor1Code'] == cameo_1) & (df['Actor2Code'] == cameo_2)]
    return df

def count_events_between_countries(actor1Name, actor2Name, date):
    events = events_between_countries(actor1Name, actor2Name, date)
    return len(events.index)


print(events_between_countries("POL", "FRA", ['2020-05-07', '2020-05-08']))

print(count_events_between_countries("POL", "FRA", ['2020-05-07', '2020-05-08']))
