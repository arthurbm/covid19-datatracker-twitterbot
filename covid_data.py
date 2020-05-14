import requests
import time
from datetime import datetime, timedelta
from time import mktime
import textwrap

lista_siglas = ['AL','AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']
lista_siglas_nordeste = ['MA', 'PI', 'PB', 'PE', 'CE', 'BA', 'AL', 'SE', 'RN']

def yesterday_string_to_datetime(data_string):
    x = time.strptime(data_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    day_last_atualization = datetime.fromtimestamp(mktime(x))
    yesterday = day_last_atualization - timedelta(days=1)
    return yesterday

#Dados de hoje do estado
def dados_covid_estado(uf):
    url = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/' + uf.lower()
    response = requests.request('GET', url)
    data_today = response.json()

    #Data de ontem 
    yesterday = yesterday_string_to_datetime(data_today['datetime'])
    yesterday = yesterday.strftime('%Y%m%d')
    
    #Dados de ontem todos os estados
    urlYest = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil/' + yesterday
    responseYest = requests.request('GET', urlYest)
    data_yest_full = responseYest.json()

    #Pegar só os dados do estado
    for dados in data_yest_full['data']:
        if (dados['uf'] == uf.upper()):
            data_yest_state = dados
            break

    #Fazendo o texto
    data_today['new_cases'] = (data_today['cases'] - data_yest_state['cases'])
    data_today['new_deaths'] = (data_today['deaths'] - data_yest_state['deaths'])
    
    text = (
        'Estado: ' + data_today['state'] + '\n' + 
        'Número de casos: ' + str(data_today['cases']) +'\n' +
        'Novos casos hoje: ' + str(data_today['new_cases']) + '\n' +
        'Número de óbitos: ' + str(data_today['deaths']) + '\n' +
        'Novos óbitos hoje: ' + str(data_today['new_deaths']) + '\n' +
        'Última atualização: ' + (data_today['datetime'])[:10] + ' (' + (data_today['datetime'])[11:16] + ')' + '\n'
    )
    
    return text, data_today

def dados_covid_city(state,city):
    url = 'https://brasil.io/api/dataset/covid19/caso/data/'
    params = {
        "format": "json",
        "state": state.upper(),
        "city": city.capitalize(),
        "place_type": "city",
        "is_last": "True",
    }
    response = requests.request('GET', url, params=params)
    data_today_complete = response.json()

    data_today = (data_today_complete['results'])[0]

    #Pegando a data de ontem
    x = time.strptime(data_today['date'], '%Y-%m-%d')
    day_last_atualization = datetime.fromtimestamp(mktime(x))
    yesterday = day_last_atualization - timedelta(days=1)
    yesterday = yesterday.strftime('%Y-%m-%d')

    paramsYest = {
        "format": "json",
        "state": state.upper(),
        "city": city.capitalize(),
        "place_type": "city",
        "date": yesterday,
    }
    responseYest = requests.request('GET', url, params=paramsYest)
    data_yest_complete = responseYest.json()

    data_yest = (data_yest_complete['results'])[0]

    data_today['new_cases'] = data_today['confirmed'] - data_yest['confirmed']
    data_today['new_deaths'] = data_today['deaths'] - data_yest['deaths']
    
    if data_today['new_cases'] == 0:
        data_today['new_cases'] = 'Não relatado'
        data_today['new_deaths'] = 'Não relatado'

    text = (
        'Cidade: ' + data_today['city'] + '\n' + 
        'Nº de casos: ' + str(data_today['confirmed']) +'\n' +
        'Novos casos hoje: ' + str(data_today['new_cases']) + '\n' +
        'Nº de óbitos: ' + str(data_today['deaths']) + '\n' +
        'Novos óbitos hoje: ' + str(data_today['new_deaths']) + '\n' +
        'índice de mortalidade: ' + str(format( data_today['death_rate'], ".2%")) + '\n'
        'Última atualização: ' + (data_today['date']) + '\n'
    )
    return text, data_today

#Vou ter que varrer os dados de yesterday, porque não dá pra passar query params
def dados_covid_estados():
    url = 'https://covid19-brazil-api.now.sh/api/report/v1'
    
    response = requests.request('GET', url)
    data_today_full = response.json()

    data_today = (data_today_full['data'])

    data_today = sorted(data_today, key = lambda i : i['cases'])
    
    #Data de ontem 
    yesterday = yesterday_string_to_datetime((data_today[0])['datetime'])
    yesterday = yesterday.strftime('%Y%m%d')

    urlYest = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil/' + yesterday

    response = requests.request('GET', urlYest)
    data_yest_full = response.json()

    data_yest = (data_yest_full['data'])
    text = []
    #Está feito dessa forma para garantir que mesmo que estados troquem de posição em relação aos casos, 
    # o algorítimo faça a correspondência certa
    for x in range(0,len(data_today) - 1):
        for y in range(0, len(data_yest) - 1):
                if ((data_yest[y])['uf']) == ((data_today[x])['uf']):
                    ((data_today[x])['new_cases']) = ((data_today[x])['cases']) - ((data_yest[y])['cases'])
                    ((data_today[x])['new_deaths']) = ((data_today[x])['deaths']) - ((data_yest[y])['deaths'])
        text.append(
        'Estado: ' + data_today[x]['state'] + '\n' + 
        'Casos: ' + str(data_today[x]['cases']) +'\n' +
        'Novos casos: ' + str(data_today[x]['new_cases']) + '\n' +
        'Obitos: ' + str(data_today[x]['deaths']) + '\n' +
        'Novos óbitos: ' + str(data_today[x]['new_deaths']) + '\n' +
        'Última atualização: ' + (data_today[x]['datetime'])[:10] + ' (' + (data_today[x]['datetime'])[11:16] + ')' + '\n'
        )

    return text, data_today

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
    
#O horári UTC é 3 horas a mais em relação a brasília
#'https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/pe'