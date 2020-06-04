from covid_data import *
import tweepy
from format_data import *
from siglas import *
import os
from os import environ

today = str(datetime.now().day) + "/" + datetime.now().strftime('%m')

CONSUMER_KEY_ONLINE = environ['CONSUMER_KEY']
CONSUMER_SECRET_ONLINE = environ['CONSUMER_SECRET']
ACESS_KEY_ONLINE = environ['ACESS_KEY']
ACESS_SECRET_ONLINE = environ['ACESS_SECRET']

auth = tweepy.OAuthHandler(CONSUMER_KEY_ONLINE, CONSUMER_SECRET_ONLINE)
auth.set_access_token(ACESS_KEY_ONLINE, ACESS_SECRET_ONLINE)
api = tweepy.API(auth)

def tweetar_dados_regiao(count, list_regiao, nome_regiao):
    try:
        states = estados_gov(count, list_regiao, nome_regiao)
        api.update_status(status= f'Estados mais afetados pelo #coronavirus na região {nome_regiao}: {today}' + states)
        print(f'Sucesso região {nome_regiao}')
    except:
        states = estados_gov((count-1), lista_siglas, nome_regiao)
        api.update_status(status = f'Estados mais afetados pelo #coronavirus na região {nome_regiao}: {today}' + states)
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

#FUNÇÃO PRINCIPAL DE TWEETS
def main_tweet():
    #Chaves estão ocultadas
    tweetar_dados_estados_geral(3)

    for lista_regiao_local, nome_regiao_local in zip(lista_regioes, lista_regioes_nomes):

        tweetar_dados_regiao(3, lista_regiao_local, nome_regiao_local)

        for lista_estados_local in lista_regiao_local:
            last_tweet_full = (api.user_timeline())[0]
            last_tweet_id = last_tweet_full.id
            tweetar_dados_cidades(3, lista_estados_local, last_tweet_id)

arquivo_id_tweet = 'last_seen.txt'
fila_last_city = 'last_city.txt'

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()

def store_city(FILE_NAME, city):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(city))
    file_write.close()

def reply():
    tweets = api.mentions_timeline(read_last_seen(arquivo_id_tweet), tweet_mode = 'extended')
    for tweet in tweets:
        if '#covid19brasil' in tweet.full_text.lower():
            print(str(tweet.id) + '-' + tweet.full_text)
            text_splited = (tweet.full_text.lower()).split('#covid19brasil')
            city = text_splited[-1]

            if city[0] == ' ':
                city.pop(0)
            
            print(city)
            try:
                text_city = cidade_gov(city)
                api.update_status(f"@{tweet.user.screen_name} {text_city}", tweet.id)
                store_city(arquivo_id_tweet, city)
                store_last_seen(arquivo_id_tweet, tweet.id)
            except:
                api.update_status('Cidade não encontrada, talvez haja erro de digitação, tente novamente')
                store_last_seen(arquivo_id_tweet, tweet.id)

#RESPONDENDO TWEETS
