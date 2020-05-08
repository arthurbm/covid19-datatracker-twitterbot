import requests
import time
from datetime import datetime, timedelta
from time import mktime

def yesterday_string_to_datetime(data_string):
    x = time.strptime(data_string, '%Y-%m-%dT%H:%M:%S.%fZ')
    day_last_atualization = datetime.fromtimestamp(mktime(x))
    yesterday = day_last_atualization - timedelta(days=1)
    return yesterday

#Dados de hoje de pernambuco
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

    #Pegar só os dados de PE
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

def dados_covid_city(uf,city):
    url = 'https://brasil.io/api/dataset/covid19/caso/data/'
    params = {
        "format": "json",
        "uf": uf.upper(),
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

    urlYest = 'https://brasil.io/api/dataset/covid19/caso/data/'
    paramsYest = {
        "format": "json",
        "uf": uf.upper(),
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

    
    

    



#O horári UTC é 3 horas a mais em relação a brasília
#'https://covid19-brazil-api.now.sh/api/report/v1/brazil/uf/pe'