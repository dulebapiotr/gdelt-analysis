import gdelt
import pandas as pd
# Version 1 queries
gd1 = gdelt.gdelt(version=1)


results= gd1.Search('2020-05-08',table='events',output='pd') # to już jest DataFrame


#liczba rodzajów wydarzeń w danym datasecie, biorę pod uwagę 2 pierwsze cyfry kodu CAMEO
# 01 - MAKE PUBLIC STATEMENT
# 02 - APPEAL
# 03 - EXPRESS INTENT TO COOPERATE
# 04 - CONSULT
# 05 - ENGAGE IN DIPLOMATIC COOPERATION
# 06 - ENGAGE IN MATERIAL COOPERATION
# 07 - PROVIDE AID
# 08 - YIELD
# 09 - INVESTIGATE
# 10 - DEMAND
# 11 - DISAPPROVE
# 12 - REJECT
# 13 - THREATEN
# 14 - PROTEST
# 15 - EXHIBIT FORCE POSTURE
# 16 - REDUCE RELATIONS
# 17 - COERCE
# 18 - ASSAULT
# 19 - FIGHT
# 20 - USE UNCONVENTIONAL MASS VIOLENCE
def count_events(data, event_type):
    if not 1<=event_type<=20:
        return 0
    events = data[['EventCode']]
    #tutaj zawężam, bo kategorie są jeszcze bardziej uszczegółowione, interesują mnie tylko pierwsze 2 cyfry kodu CAMEO
    filtered = events.apply(lambda x:  int(x['EventCode'][:2]) , axis=1) 
    checked = filtered.apply(lambda x: 1 if x == event_type else 0 )
    return checked.sum()

print(count_events(results, 21))


