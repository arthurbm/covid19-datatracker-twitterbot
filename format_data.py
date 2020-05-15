from covid_data import *
from siglas import dict_siglas
import textwrap

def estados(count, region_list):

    dict_states = dados_covid_estados_brasilio()
    text = ''
    count2 = 1

    for dict_local in dict_states:
        if count <= 0:
            break
        if dict_local['state'] in region_list:
            text += (textwrap.dedent(
                    f"""
                    {count2}) {dict_siglas[dict_local['state']]}:
                    Casos: {str(dict_local['confirmed'])} ({str(dict_local['new_cases'])} novos)
                    Óbitos: {str(dict_local['deaths'])} ({str(dict_local['new_deaths'])} novas)

                    """
                )
            )
            count -= 1
            count2 +=1
    #text_array = text.split('\n\n')
    
    text_array = text.split('\n\n')
    return text


def cidades(count, state):
    dict_cities = dados_covid_cidades(state)
    count2 = 1
    text = ''
    for dict_local in dict_cities:
        if count <= 0:
                break
        text += (textwrap.dedent(
            f"""
            {count2}) {dict_local['city']}
            Casos: {str(dict_local['confirmed'])}
            Óbitos: {str(dict_local['deaths'])}
            """
            )
        )
        count -=1
        count2 +=1

    return text

