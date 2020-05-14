from covid_data import *

def estados(count, region_list):
    dict_states = dados_covid_estados_brasilio()
    text = ''

    if count == 3:
        for dict_local in dict_states:
            if count <= 0:
                break
            if dict_local['state'] in region_list:
                text += (
                    'Estado: ' + dict_local['state'] + '\n' + 
                    'Casos: ' + str(dict_local['confirmed']) +'\n' +
                    'Novos casos: ' + str(dict_local['new_cases']) + '\n' +
                    'Obitos: ' + str(dict_local['deaths']) + '\n' +
                    'Novos óbitos: ' + str(dict_local['new_deaths']) + '\n' 
                )
                count-=1
        #print(dict_states)
        text_array = text.split('\n\n')
        return text

    elif count == 5:
        for dict_local in dict_states:
            if count <= 0:
                break
            if dict_local['state'] in region_list:
                text += (
                    'Estado: ' + dict_local['state'] + '\n' + 
                    'Casos: ' + str(dict_local['confirmed']) +'\n' +
                    'Obitos: ' + str(dict_local['deaths']) + '\n\n'
                )
                count-=1
        #print(dict_states)
        text_array = text.split('\n\n')
        return text
