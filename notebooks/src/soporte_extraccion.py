import pandas as pd
import numpy as np

import random
from random import randint
import string
import requests
from tqdm import tqdm

from time import sleep
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


import warnings
warnings.filterwarnings('ignore')



class Extraccion:
    def  __init__(self):
        pass

    def fever():
        '''
        Extrae la información principal de cada uno de los item presentes en las categorías elegidas de la web de Fever.
        '''
        
        driver = webdriver.Chrome("chromedriver.exe")
        num_res= list(range(1, 10000))
        dicc_fever= {"categoria" : [],
                     "nombre"    : [],
                     "url"       : [],
                     "precio"    : [],
                     "fecha"     : [],
                     "rating"    : []                              
                     }
        
        categorias= ["conciertos-festivales", 
                     "cultura-arte-moda", 
                     "terrazas-y-rooftops", 
                     "vida-nocturna-clubs",
                     "fabrik",
                     "monologos",
                     "parque-atracciones",
                     "brunch",
                     "deportes-aventura",
                     "teatro-eslava",
                     "musicales",
                     "exposiciones",
                     "actividades-juegos",
                     "gastronomia",
                     "cine",
                     "bebidas-afterwork",
                     "planes-aire-libre",
                     "magia-mentalismo",
                     "teatro",
                     "museos-galerias-arte",
                     "belleza-bienestar",
                     "autocine",
                     "festivales",
                     "la-chocita-del-loro",
                     "flamenco",
                     "teatro-comedia-espectaculos"]
        for categoria in categorias:
        
            driver.get(f"https://feverup.com/es/madrid/{categoria}")
            try:
                driver.find_element("xpath", '//*[@id="cookie-advice"]/button').click()
                sleep(7)
            except:
                pass
            
            
            for i in tqdm(num_res):
                try:
                
                    dicc_fever["nombre"].append(driver.find_element("xpath", f'/html/body/app-root/main/div/app-what-plan-filter/div[2]/app-what-plan-filter-list/ul/li[{i}]/app-plan-card/a/div/header/h3').text)
                    dicc_fever["url"].append(driver.find_element("xpath", f"/html/body/app-root/main/div/app-what-plan-filter/div[2]/app-what-plan-filter-list/ul/li[{i}]/app-plan-card/a").get_attribute('href'))
                    dicc_fever["categoria"].append(categoria)
                    try:
                        dicc_fever["precio"].append(driver.find_element("xpath", f"/html/body/app-root/main/div/app-what-plan-filter/div[2]/app-what-plan-filter-list/ul/li[{i}]/app-plan-card/a/div/footer/div[2]/app-plan-price/div").text)
                    except:
                        dicc_fever["precio"].append(np.nan)
                    try:
                        dicc_fever["fecha"].append(driver.find_element("xpath", f"/html/body/app-root/main/div/app-what-plan-filter/div[2]/app-what-plan-filter-list/ul/li[{i}]/app-plan-card/a/div/header/ul/li").text)
                    except:
                        dicc_fever["fecha"].append(np.nan)
                    try:
                        dicc_fever["rating"].append(driver.find_element("xpath", f"/html/body/app-root/main/div/app-what-plan-filter/div[2]/app-what-plan-filter-list/ul/li[{i}]/app-plan-card/a/div/footer/div[1]/ul/li/app-plan-review-stars/div/span[1]").text)
                    except:
                        dicc_fever["rating"].append(np.nan)
                        driver.execute_script("window.scrollBy(0, 5000);")
                    sleep(randint(3,5))

                except NoSuchElementException:
                    print(f"Fin {categoria}")
                    print(f"Element not found {i}")
                    break
                
        df_fever= pd.DataFrame(dicc_fever)
        df_fever.to_csv(f'../data/FEVER.csv', header=True, index=False)
    
    
    def fever_detalle():
        '''
        Extrae el detalle de cada uno de los item o planes de Fever a través de las url.
        '''

        df= pd.read_csv(f'../data/FEVER.csv')
        lista_url=list(df["url"].unique())
        
        sopa_ini=[]

        for url in tqdm(lista_url):
            sopa_ini.append(requests.get(url))
            sleep(randint(3,7))
        
        sopa=[]

        for s in tqdm(sopa_ini):
            sopa.append(BeautifulSoup(s.content, 'html.parser'))

        dicc_fever_detalle= {"descripcion":[],
                             "sku"        :[],
                             "imagen"     :[],
                             "latitud"    :[],
                             "longitud"   :[],
                             "lugar"      :[]
                            }

        for plan in tqdm(sopa):
            try:
                description = plan.find('script', {'type': 'application/ld+json'}).string
                description_dict = json.loads(description)

                try:
                    description_text = description_dict['description']
                    descripcion_inicio = description_text.find("Descripción") + len("Descripción")
                    descripcion_fin = description_text.find("sku") 
                    dicc_fever_detalle["descripcion"].append(description_text[descripcion_inicio:descripcion_fin])
                except:
                    dicc_fever_detalle["descripcion"].append(np.nan)

                try:  
                    dicc_fever_detalle["sku"].append(description_dict['sku'])
                except:
                    dicc_fever_detalle["sku"].append(np.nan)

                try:  
                    dicc_fever_detalle["imagen"].append(description_dict['image']['contentURL'])
                except:
                    dicc_fever_detalle["imagen"].append(np.nan)

                try:  
                    dicc_fever_detalle["latitud"].append(description_dict['image']['contentLocation']['geo']['latitude'])
                    dicc_fever_detalle["longitud"].append(description_dict['image']['contentLocation']['geo']['longitude'])
                except:
                    dicc_fever_detalle["latitud"].append(np.nan)
                    dicc_fever_detalle["longitud"].append(np.nan)

                try:  
                    dicc_fever_detalle["lugar"].append(description_dict['offers'][0]['areaServed']['name'])
                except:
                    dicc_fever_detalle["lugar"].append(np.nan)

            except:
                pass
        
        df_fever_detalle= pd.DataFrame(dicc_fever_detalle)
        df_fever_detalle.to_csv(f'../data/FEVER_DETALLE.csv', header=True, index=False)


    def groupon():
        '''
        Extrae la información principal de cada uno de los item presentes en las categorías elegidas de la web de Groupon.
        '''

        driver = webdriver.Chrome("chromedriver.exe")
        num_res= list(range(1, 1000))

        dicc_groupon= { "categoria" : [],
                        "nombre"    : [],
                        "direccion" : [],
                        "url"       : [],
                        "precio"    : [],
                        "precio_2"  : [],
                        "rating"    : []                              
                       }

        categorias= ["juegos-de-escape", 
                     "cursos-fotorgrafia", 
                     "clases-baile", 
                     "v-cata-de-vinos",
                     "v-espectaculos",
                     "carreras",
                     "bolos",
                     "paintball",
                     "equitacion",
                     "v-escalada",
                     "v-esqui-y-snowboard",
                     "deportes-acuaticos",
                     "patinaje-sobre-hielo",
                     "v-golf",
                     "parapente",
                     "tours-de-vinos",
                     "excursiones-por-la-ciudad-y-lugares-de-interes",
                     "excursiones-y-aventuras-al-aire-libre",
                     "tour-de-vuelo",
                     "day-spa"
                     ]


        for categoria in categorias:
        
            driver.get(f"https://www.groupon.es/ofertas/{categoria}?distance=%5B0.0..50.0%5D")

            try:
                driver.find_element("xpath", '//*[@id="nothx"]').click()
                sleep(6)
            except:
                pass
            
            try:
                driver.find_element("xpath", '//*[@id="gdpr-accept"]').click()
                sleep(3)
            except:
                pass
            
            for i in tqdm(num_res):
                try:
                
                    dicc_groupon["nombre"].append(driver.find_element("xpath", f'//*[@id="pull-deal-feed"]/figure[{i}]/div/a/div[2]/div[1]/div').text)
                    dicc_groupon["direccion"].append(driver.find_element("xpath", f'//*[@id="pull-deal-feed"]/figure[{i}]/div/a/div[2]/div[2]/div/span[1]').text)
                    dicc_groupon["url"].append(driver.find_element("xpath", f'//*[@id="pull-deal-feed"]/figure[{i}]/div/a').get_attribute('href'))
                    dicc_groupon["categoria"].append(categoria)

                    try:
                        dicc_groupon["precio"].append((driver.find_element("xpath", f'//*[@id="pull-deal-feed"]/figure[{i}]/div/a/div[2]/div[4]/div[1]/div[1]/div[2]/span').text))

                    except:
                        dicc_groupon["precio"].append(np.nan)

                    try:
                        dicc_groupon["precio_2"].append(driver.find_element("xpath", f'//*[@id="pull-deal-feed"]/figure[{i}]/div/a/div[2]/div[4]/div[1]/div[2]/div[2]/div[2]').text)

                    except:
                        dicc_groupon["precio_2"].append(np.nan)

                    try:
                        dicc_groupon["rating"].append(driver.find_element("xpath", f'//*[@id="pull-deal-feed"]/figure[{i}]/div/a/div[2]/div[3]/div/div[1]').text)
                    except:
                        dicc_groupon["rating"].append(np.nan)


                    sleep(randint(3,5))

                except NoSuchElementException:
                    print(f"Fin {categoria}")
                    print(f"Element not found {i}")
                    break
                
                
        df_groupon= pd.DataFrame(dicc_groupon)
        df_groupon.to_csv(f'../data/GROUPON.csv', header=True, index=False)

    
    def groupon_detalle():
        '''
        Extrae el detalle de cada uno de los item o planes de Groupon a través de las url.
        '''

        df= pd.read_csv(f'../data/GROUPON.csv')
        lista_url=list(df["url"].unique())

        driver = webdriver.Chrome("chromedriver.exe")

        dicc_groupon_detalle= { "url"        :[],
                                "descripcion":[],
                                "imagen"     :[]
                              }

        for url in tqdm(lista_url):

            driver.get(url)

            try:
                driver.find_element("xpath", '//*[@id="nothx"]').click()
                sleep(6)
            except:
                pass
            
            try:
                driver.find_element("xpath", '//*[@id="gdpr-accept"]').click()
                sleep(3)
            except:
                pass
            
            try:
            
                dicc_groupon_detalle["url"].append(url)

                try:
                    dicc_groupon_detalle["imagen"].append(driver.find_element("xpath", f'//*[@id="overflow-container"]/div/div/img').get_attribute("src"))
                except:
                    dicc_groupon_detalle["imagen"].append(np.nan)

                try:
                    dicc_groupon_detalle["descripcion"].append(driver.find_element("xpath", f'//*[@id="deal-pitch"]').text)
                except:
                    dicc_groupon_detalle["descripcion"].append(np.nan)

                sleep(randint(3,5))

            except NoSuchElementException:
                print(f"Element not found {url}")
                break
            
        df_groupon_detalle= pd.DataFrame(dicc_groupon_detalle)
        df_groupon_detalle.to_csv(f'../data/GROUPON_DETALLE.csv', header=True, index=False)

    def tripadvisor_detalle():
        '''
        Extrae el detalle de cada uno de los item o restaurantes de Tripadvisor a través de las url.
        '''

        df = pd.read_json('tutorial/TRIPADVISOR_DETALLE.json')
        df['url'] = 'https://www.tripadvisor.es' + df['url']
        lista_url=list(df["url"].unique())

        dicc_trip=  {"url"          : [],
                     "coordenadas"  : [],
                     "imagen"       : []                             
                     }
        
        driver = webdriver.Chrome("chromedriver.exe")


        for url in tqdm(lista_url):

            driver.get(url)

            sleep(randint(2,4))
            try:
                driver.find_element("xpath", '//*[@id="onetrust-accept-btn-handler"]').click()

            except:
                pass
            
            dicc_trip["url"].append(url)

            try:
                dicc_trip["coordenadas"].append(driver.find_element("xpath", f'//*[@id="component_54"]/div[1]/div/div[3]/div/div/span[1]/span/img').get_attribute("src"))
            except NoSuchElementException:
                try:
                    dicc_trip["coordenadas"].append(driver.find_element("xpath", f'//*[@id="component_56"]/div[1]/div/div[3]/div/div/span[1]/span/img').get_attribute("src"))
                except NoSuchElementException:
                    try:
                        dicc_trip["coordenadas"].append(driver.find_element("xpath", f'//*[@id="component_55"]/div[1]/div/div[3]/div/div/span[1]/span/img').get_attribute("src"))
                    except NoSuchElementException:
                        dicc_trip["coordenadas"].append(np.nan)
                        print(f"no coordenadas {url}")

            try:
                dicc_trip["imagen"].append(driver.find_element("xpath", f'//*[@id="taplc_resp_rr_photo_mosaic_0"]/div/div[1]/div[1]/div[2]/div[2]/div[1]/div/img').get_attribute("src"))

            except NoSuchElementException:
                try:
                    dicc_trip["imagen"].append(driver.find_element("xpath", f'//*[@id="taplc_resp_rr_photo_mosaic_0"]/div/div[1]/div[1]/div[2]/div[3]/div/div/img').get_attribute("src"))
                except NoSuchElementException:
                    dicc_trip["imagen"].append(np.nan)
                    print(f"no imagen {url}")

        df_trip_detalle= pd.DataFrame(dicc_trip)
        df_trip_detalle.to_csv(f'../data/TRIPADVISOR_DETALLE.csv', header=True, index=False)