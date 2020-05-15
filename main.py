from covid_data import *
import tweepy
from twitterKeys import *
from format_data import estados,cidades
from siglas import *

def tweetar_dados_regiao(count, list_regiao, nome_regiao):
    try:
        states = estados(count, list_regiao)
        api.update_status(status= f'Estados mais graves {nome_regiao}: \n\n' + states)
    except:
        states = estados(3, lista_siglas)
        api.update_status(status = f'Estados mais graves {nome_regiao}: \n\n' + states)

    
def tweetar_dados_estados_geral(count):
    states = estados(count, lista_siglas)
    api.update_status(status= 'Estados mais graves Brasil: \n\n' + states)

def tweetar_dados_cidades(count, state):
    cities = cidades(count, state)
    api.update_status(status= f'Cidades mais afetadas {dict_siglas[state]}: \n\n' + cities)

#########################################################################################

#Chaves estão ocultadas
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)
api = tweepy.API(auth)

tweetar_dados_estados_geral(3)

for lista_regiao_local, nome_regiao_local in zip(lista_regioes, lista_regioes_nomes):
    tweetar_dados_regiao(4, lista_regiao_local, nome_regiao_local)

for lista_estados_local in lista_siglas_nordeste:
    tweetar_dados_cidades(4, lista_estados_local)
