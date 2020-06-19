from tweet_functions import *

#FUNÇÕES DE TESTE
def test_results():
    #print(estados(len(lista_siglas), lista_siglas))
    x = estados_gov(25, lista_siglas)
    print(x)

def test_results_thread():
    last_tweets = api.user_timeline()
    for some_tweet in last_tweets:
        print(f"Id: {some_tweet.id}\nText: {some_tweet.text}\n")

#RODANDO A FUNÇÃO

while True:
    one_day = 60 * 60 * 24
    main_tweet()
    time.sleep(one_day)