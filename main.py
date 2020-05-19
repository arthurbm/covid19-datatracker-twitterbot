from covid_data import *
import tweepy
from twitterKeys import *
from format_data import *
from siglas import *
from datetime import datetime
today = str(datetime.now().day) + "/" + datetime.now().strftime('%m')

def tweetar_dados_regiao(count, list_regiao, nome_regiao):
    try:
        states = estados_gov(count, list_regiao)
        api.update_status(status= f'Estados mais afetados pelo #coronavirus em {nome_regiao}: {today}\n\n' + states)
    except:
        states = estados_gov((count-1), lista_siglas)
        api.update_status(status = f'Estados mais afetados pelo #coronavirus em {nome_regiao}:{today}\n\n' + states)

def tweetar_dados_estados_geral(count):
    try:
        states = estados_gov(count, lista_siglas)
        api.update_status(status= f'Estados mais afetados pelo #coronavirus no Brasil: {today}\n\n' + states)
    except:
        states = estados_gov(count-1, lista_siglas)
        api.update_status(status= f'Estados mais afetados pelo #coronavirus no Brasil: {today}\n\n' + states)

def tweetar_dados_cidades(count, state, tweet_id):
    try:
        cities = cidades(count, state)
        api.update_status((f'Cidades mais afetadas pelo #coronavirus em {dict_siglas[state]}: {today}\n' + cities), in_reply_to_status_id = tweet_id)
    except:
        cities = cidades(count-1, state)
        api.update_status((f'Cidades mais afetadas pelo #coronavirus em {dict_siglas[state]}: {today}\n' + cities), in_reply_to_status_id = tweet_id)


#########################################################################################
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)
api = tweepy.API(auth)

def main_tweet():
    #Chaves estão ocultadas
    tweetar_dados_estados_geral(3)

    for lista_regiao_local, nome_regiao_local in zip(lista_regioes, lista_regioes_nomes):
        tweetar_dados_regiao(3, lista_regiao_local, nome_regiao_local)

        for lista_estados_local in lista_regiao_local:
            last_tweet_full = (api.user_timeline())[0]
            last_tweet_id = last_tweet_full.id
            tweetar_dados_cidades(3, lista_estados_local, last_tweet_id)

    #for lista_estados_local in lista_siglas_nordeste:
    #    tweetar_dados_cidades(3, lista_estados_local)

    #for lista_regiao in lista_regioes:
    #    for lista_estados_local in lista_regiao:
    #        tweetar_dados_cidades(4, lista_estados_local)

        

def test_results():
    #print(estados(len(lista_siglas), lista_siglas))
    print(estados(25, lista_siglas))

def test_results_thread():
    last_tweets = api.user_timeline()
    for some_tweet in last_tweets:
        print(f"Id: {some_tweet.id}\nText: {some_tweet.text}\n")

main_tweet()