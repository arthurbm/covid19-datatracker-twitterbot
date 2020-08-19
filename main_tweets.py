from tweet_functions import *

#FUNÇÕES DE TESTE
def test_results():
    #print(estados(len(lista_siglas), lista_siglas))
    x = estados_gov(25, lista_siglas)
    print(x)

def test_results_timeline():
    last_tweets = api.user_timeline(tweet_mode = 'extended')
    for some_tweet in last_tweets:
        print(f"Id: {some_tweet.id}\nText: {some_tweet.full_text}\n")

#RODANDO A FUNÇÃO

test_results()

#while True:
#    one_day = 60 * 60 * 24
#    main_tweet()
#    time.sleep(one_day)