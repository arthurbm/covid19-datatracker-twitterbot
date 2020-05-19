from covid_data import *
from siglas import dict_siglas
import textwrap

def estados_gov(count, region_list):
    dict_states = dados_estados_gov()
    text = ''
    count2 = 1

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
#Usado para mostrar os principais estados em cada região
def estados(count, region_list):
    dict_states = dados_covid_estados_brasilio()
    text = ''
    count2 = 1
    count_desatualizados = 0
    count_erro = 0
    count_atualizados = 0
    estados_desatalizados = []
    estados_erro = []
    estados_atualizados = []

    for dict_local in dict_states:
        if count <= 0:
            break
        if (dict_local['state'] in region_list):
            try:
                if dict_local['new_cases'] != 0:
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
                    count_atualizados +=1
                    estados_atualizados.append(dict_siglas[dict_local['state']])
                #Casos de estados que não foram atualizados
                else:
                    text += (textwrap.dedent(
                            f"""
                            {count2}) {dict_siglas[dict_local['state']]}:
                            Casos: {str(dict_local['confirmed'])}
                            Óbitos: {str(dict_local['deaths'])}

                            """
                        )
                    )
                    count -= 1
                    count2 +=1
                    count_desatualizados +=1
                    estados_desatalizados.append(dict_siglas[dict_local['state']])
            #Estados que não tem o new cases e new deaths por algum motivo
            except:
                text += (textwrap.dedent(
                        f"""
                        {count2}) {dict_siglas[dict_local['state']]}:
                        Casos: {str(dict_local['confirmed'])}
                        Óbitos: {str(dict_local['deaths'])}

                        """
                    )
                )
                count -= 1
                count2 +=1
                count_erro +=1
                estados_erro.append(dict_siglas[dict_local['state']])
    #text_array = text.split('\n\n')
    
    text_array = text.split('\n\n')
    print(f'Número de estados sem atualização: {count_desatualizados}\nEstados desatualizados: {estados_desatalizados}\n')
    print(f'Número de estados atualizados: {count_atualizados}\nEstados atualizados: {estados_atualizados}\n')
    print(f'Número de estados com erro: {count_erro}\nEstados desatualizados: {estados_erro}\n')
    
    return text


def cidades(count, state):
    dict_cities = dados_covid_cidades(state)
    dict_states = dados_estados_gov()
    count2 = 1

    for dict_state_local in dict_states:
        if dict_state_local['nome'] == (state.upper()):
            dict_state_unico = dict_state_local

    text = f'Nº de Casos: {dict_state_unico["casosAcumulado"]}\nNº de Óbitos: {dict_state_unico["obitosAcumulado"]}\n\n'

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



