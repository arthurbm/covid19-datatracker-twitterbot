from covid_data import *

uf = input('Digite o UF do estado: \n')
city = input('Digite a cidade: \n')
text_state, discionario = dados_covid_estado(uf)
text_city, dict_city = dados_covid_city(uf,city)
text_states, dict_states = dados_covid_estados()
print(text_state)
print(text_city)
print('Estados nordestinos:\n')


for text_local, dict_local in zip(text_states, dict_states):
    if dict_local['uf'] in lista_siglas_nordeste:
        print(text_local)
