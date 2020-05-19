from covid_data import *
import tweepy
from twitterKeys import *
from format_data import *
from siglas import *

today = str(datetime.now().day) + "/" + datetime.now().strftime('%m')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)
api = tweepy.API(auth)

def tweetar_dados_regiao(count, list_regiao, nome_regiao):
    try:
        states = estados_gov(count, list_regiao)
        api.update_status(status= f'Estados mais afetados pelo #coronavirus na região {nome_regiao}: {today}\n\n' + states)
        print(f'Sucesso região {nome_regiao}')
    except:
        states = estados_gov((count-1), lista_siglas)
        api.update_status(status = f'Estados mais afetados pelo #coronavirus na região {nome_regiao}:{today}\n\n' + states)
        print(f'Sucesso com excesso região {nome_regiao}')

def tweetar_dados_estados_geral(count):
    try:
        states = estados_gov(count, lista_siglas)
        api.update_status(status= f'Estados mais afetados pelo #coronavirus no Brasil: {today}\n\n' + states)
        print('Sucesso estados mais graves Brasil')
    except:
        states = estados_gov(count-1, lista_siglas)
        api.update_status(status= f'Estados mais afetados pelo #coronavirus no Brasil: {today}\n\n' + states)
        print('Sucesso com excesso estados mais graves Brasil')

def tweetar_dados_cidades(count, state, tweet_id):
    try:
        cities = cidades(count, state)
        api.update_status((f'Cidades mais afetadas pelo #coronavirus em {dict_siglas[state]}: {today}\n' + cities), in_reply_to_status_id = tweet_id)
        print(f'Sucesso cidades de {dict_siglas[state]}')
    except:
        cities = cidades(count-1, state)
        api.update_status((f'Cidades mais afetadas pelo #coronavirus em {dict_siglas[state]}: {today}\n' + cities), in_reply_to_status_id = tweet_id)
        print(f'Sucesso com excesso cidades de {dict_siglas[state]}')

#RESPONDENDO TWEETS


