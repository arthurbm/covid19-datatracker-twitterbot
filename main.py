from covid_data import *
import tweepy
from twitterKeys import *
from format_data import estados

#Count deve ser um inteiro

def tweetar_dados_nordeste():
    states = estados(5, lista_siglas_nordeste)
    api.update_status(status= 'Estados mais graves nordeste: \n\n' + states)

def tweetar_dados_estados():
    states = estados(5, lista_siglas)
    api.update_status(status= 'Estados mais graves Brasil: \n\n' + states)

#Chaves estão ocultadas
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACESS_KEY, ACESS_SECRET)
api = tweepy.API(auth)

tweetar_dados_nordeste()