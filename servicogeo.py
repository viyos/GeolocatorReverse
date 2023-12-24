import geopandas as gpd
from shapely.geometry import Polygon
import pandas as pd
import requests
import json
import time
import warnings

warnings.filterwarnings("ignore")

# Read the shapefile
gdf = gpd.read_file(r'Setorização_de_Risco.shp')

dados = pd.DataFrame(gdf)
#Remove missing value
dados.dropna(subset = ['munic'], inplace=True)

cepstotal = []

for row in dados.itertuples():

    latlong = str(row.geometry)

    estado = str(row.uf)

    cidade = str(row.munic)

    latlong = latlong.replace('POLYGON ((','').replace('MULTIPOLYGON (((','').replace('(((','').replace('((','').replace('))','').replace(')))','')

    latlong = latlong.split(',')

    lista_ceps = []

    for i in latlong:
        latitlongit = i.strip() #Remove espaços depois e antes das strings
        latitlongit = latitlongit.split(' ') #Separa os elementos da string que estão com um espaçamento
        latitude = latitlongit[1]
        longitude = latitlongit[0]
        print(f'Latitude: {latitude}, Longitude: {longitude}')
        try:
            endereco = requests.get(f"https://geocode.maps.co/reverse?lat={latitude}&lon={longitude}",verify=False)
            endereco = endereco.json()
            logradouro = str(endereco['address']['road'])
            cidade = cidade
            estado = estado
            time.sleep(1)
            cepreq = requests.get(f"https://viacep.com.br/ws/{estado}/{cidade}/{logradouro}/json/",verify=False)
            cepreq = cepreq.json()
            print(cepreq)
            cep = cepreq[0]['cep']
            lista_ceps.append(cep)
        except:
            pass
    lista_ceps = list(set(lista_ceps))
    cepstotal.append(lista_ceps)
    print(f'Lista total: {cepstotal}')

lis = pd.Series({'CEP': cepstotal})
dfCEP = pd.DataFrame([lis])
dados['CEP'] = dfCEP['CEP']
dados.to_csv(r"SGBDOfc.csv", index=False,sep=';',encoding='utf-8-sig')