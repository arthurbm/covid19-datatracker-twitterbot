import requests
import time
from datetime import datetime, timedelta
from time import mktime
import textwrap

def yesterday_string_to_datetime(data_string):
    x = time.strptime(data_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    day_last_atualization = datetime.fromtimestamp(mktime(x))
    yesterday = day_last_atualization - timedelta(days=1)
    return yesterday

def dados_estados_gov():
    url = 'https://xx9p7hp1p7.execute-api.us-east-1.amazonaws.com/prod/PortalEstado'

    response = requests.request('GET', url)
    data_today_full = response.json()

    return data_today_full

def dados_covid_estados_brasilio():
    url = 'https://brasil.io/api/dataset/covid19/caso/data/'
    params = {
        "format": "json",
        "place_type": "state",
        "is_last": "True",
    }
    
    response = requests.request('GET', url, params = params)
    data_today_full = response.json()

    data_today = (data_today_full['results'])

    data_today_sorted = sorted(data_today, key = lambda i : (i['confirmed']), reverse = True)

    #Data de ontem
    x = time.strptime((data_today_sorted[10])['date'], '%Y-%m-%d')
    day_last_atualization = datetime.fromtimestamp(mktime(x))
    yesterday = day_last_atualization - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    urlYest = 'https://brasil.io/api/dataset/covid19/caso/data/'
    paramsYest = {
        "format": "json",
        "place_type": "state",
        "date": yesterday,
    }

    response = requests.request('GET', urlYest, params = paramsYest)
    data_yest_full = response.json()

    data_yest = (data_yest_full['results'])

    #Está feito dessa forma para garantir que mesmo que estados troquem de posição em relação aos casos, 
    # o algorítimo faça a correspondência certa
    for x in range(0,len(data_today_sorted)):
        for y in range(0, len(data_yest)):
                if ((data_yest[y])['state']) == ((data_today_sorted[x])['state']):
                    ((data_today_sorted[x])['new_cases']) = ((data_today_sorted[x])['confirmed']) - ((data_yest[y])['confirmed'])
                    ((data_today_sorted[x])['new_deaths']) = ((data_today_sorted[x])['deaths']) - ((data_yest[y])['deaths'])

    return data_today_sorted

def dados_covid_cidades(state):
    url = 'https://brasil.io/api/dataset/covid19/caso/data/'
    params = {
        "format": "json",
        "place_type": "city",
        "is_last": "True",
        "state": state
    }

    response = requests.request('GET', url, params = params)
    data_today_full = response.json()

    data_today = (data_today_full['results'])

    data_today_sorted = sorted(data_today, key = lambda i : (i['confirmed']), reverse = True)

    return data_today_sorted
    
#O horári UTC é 3 horas a mais em relação a brasília

##############################################################################################################

