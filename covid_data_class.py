import requests
import time
from datetime import datetime, timedelta
from time import mktime
from covid_data import yesterday_string_to_datetime

class TwitterBot():
    def __init__(self):
        self.data_states = []
        self.data_cities = []
    
    def get_data_states(self):
        url = 'https://covid19-brazil-api.now.sh/api/report/v1'
    
        response = requests.request('GET', url)
        data_today_full = response.json()

        data_today = (data_today_full['data'])

        data_today_sorted = sorted(data_today, key = lambda i : i['cases'])
        
        #Data de ontem 
        yesterday = yesterday_string_to_datetime((data_today[0])['datetime'])
        yesterday = yesterday.strftime('%Y%m%d')

        urlYest = 'https://covid19-brazil-api.now.sh/api/report/v1/brazil/' + yesterday

        response = requests.request('GET', urlYest)
        data_yest_full = response.json()

        data_yest = (data_yest_full['data'])

        for x in range(0,len(data_today) - 1):
            for y in range(0, len(data_yest) - 1):
                    if ((data_yest[y])['state']) ==(data_today[x])['state']:
                        (data_today[x])['new_cases'] = (data_today[x])['cases'] -(data_yest[y])['cases']
                        (data_today[x])['new_deaths'] = (data_today[x])['deaths'] -(data_yest[y])['deaths']

        
        
        self.data_states = data_today