from covid_data import *
from siglas import dict_siglas

#Usado para mostrar os principais estados em cada região
def estados_gov(count, region_list, region_name=None):
    dict_states = dados_estados_gov()
    dict_sintese = (dados_covid_sintese())[1:]
    text = ''
    count2 = 1

    for dict_sintese_local in dict_sintese:
        if dict_sintese_local['_id'] == region_name:
            text+= (
                textwrap.dedent(
                    f"""
                    Nº de Casos: {dict_sintese_local['casosAcumulado']}
                    Nº de Óbitos: {dict_sintese_local['obitosAcumulado']}

                    """
                )
            )

    for dict_local in dict_states:
        if count <= 0:
            break
        if (dict_local['nome'] in region_list):
            text += (
                textwrap.dedent(
                    f"""
                    {count2}) {dict_siglas[dict_local['nome']]}:
                    Casos: {str(dict_local['casosAcumulado'])}
                    Óbitos: {str(dict_local['obitosAcumulado'])}
                    
                    """
                )
            )
            count -=1
            count2 +=1
    
    return text

#Usado para retornar os dados de apenas uma cidade
def cidade(city):
    dict_city = dados_covid_city_gov(city)

    text = (
        textwrap.dedent(
            f"""
            Cidade: {dict_city['nome']}
            Número de casos: {dict_city['casosAcumulado']}
            Número de óbitos: {dict_city['obitosAcumulado']}
            """
        )
    )

    return text

def cidades(count, state):
    dict_cities_brasil_io = dados_covid_cidades(state)
    dict_cities_gov = dados_covid_city_gov_full()
    dict_states = dados_estados_gov()
    count2 = 1

    for dict_state_local in dict_states:
        if dict_state_local['nome'] == (state.upper()):
            dict_state_unico = dict_state_local

    text = f'Nº de Casos: {dict_state_unico["casosAcumulado"]}\nNº de Óbitos: {dict_state_unico["obitosAcumulado"]}\n\n'

    for dict_city_brasil_io in dict_cities_brasil_io:
        if count <= 0:
                break

        dict_city_gov_unico = {}
        #Procuro na API do governo a cidade que está sendo analizada no respectivo loop da Brail io
        for dict_city_gov in dict_cities_gov:
            if dict_city_gov['nome'] == dict_city_brasil_io['city']:
                dict_city_gov_unico = dict_city_gov
                break

        #Estou fazendo isso para o caso de ele não achar a cidade
        if dict_city_gov_unico == {}:
            continue

        text += (
            textwrap.dedent(
                f"""
                {count2}) {dict_city_gov_unico['nome']}
                Casos: {dict_city_gov_unico['casosAcumulado']}
                Óbitos: {dict_city_gov_unico['obitosAcumulado']}
                """
            )
        )
        count -=1
        count2 +=1

    return text


