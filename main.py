from covid_data import dados_covid_estado,dados_covid_city

uf = input('Digite o UF do estado: \n')
city = input('Digite a cidade: \n')
text_state, discionario = dados_covid_estado(uf)
text_city, dict_city = dados_covid_city(uf,city)
print(text_state)
print(text_city)
#print(dados_covid_city('PE','Recife'))