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
    