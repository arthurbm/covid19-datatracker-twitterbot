from tweet_functions import *

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

#FUNÇÕES DE TESTE
def test_results():
    #print(estados(len(lista_siglas), lista_siglas))
    x = estados_gov(25, lista_siglas)
    print(x)

def test_results_thread():
    last_tweets = api.user_timeline()
    for some_tweet in last_tweets:
        print(f"Id: {some_tweet.id}\nText: {some_tweet.text}\n")

arquivo_id_tweet = 'last_seen.txt'

def read_last_seen(FILE_NAME):
    file_read = open(FILE_NAME, 'r')
    last_seen_id = int(file_read.read().strip())
    file_read.close()
    return last_seen_id

def store_last_seen(FILE_NAME, last_seen_id):
    file_write = open(FILE_NAME, 'w')
    file_write.write(str(last_seen_id))
    file_write.close()

def reply():
    tweets = api.mentions_timeline(read_last_seen(arquivo_id_tweet), tweet_mode = 'extended')
    for tweet in tweets:
        if '#covidbrasilcidades' in tweet.full_text.lower():
            print(str(tweet.id) + '-' + tweet.full_text)
            api.update_status(f"@{tweet.user.screen_name} Auto reply works :)", tweet.id)
            store_last_seen(arquivo_id_tweet, tweet.id)

#RODANDO AS FUNÇÕES
main_tweet()