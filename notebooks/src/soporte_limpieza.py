from geopy.geocoders import Nominatim
import re
import nltk
from nltk.corpus import stopwords
from time import sleep
import pandas as pd




class Limpieza:
    def  __init__(self):
        pass


    def extract_sku(url):
        '''
        Se utilizará esta función en la limpieza de los datos de Fever. El output de la misma es la parte de la URL correspondiente a la SKU para
        unir df_fever y df_detalle. El input será una url.
        '''    
        match = re.search(r'\d+$', url)
        if match:
            return match.group()
        else:
            return None
    
    def columna_precio_fever(precio):
        '''
        Se utilizará esta función en la limpieza de la columna de precio en los datos de Fever.
        '''  
        patron = r'(Desde\n)?(\d+,\d+)'
    
        if precio is None:
            return 0
        elif isinstance(precio, str):
            match = re.search(patron, precio)
            if match:
                return float(match.group(2).replace(',', '.'))
            else:
                return 0
        else:
            return 0
    
    def columna_rating(rating):
        '''
        Se utilizará esta función en la limpieza de la columna de rating en los datos de Fever y Groupon.
        '''  
        if pd.isna(rating):
            return 0.0
        else:
            match = re.match(r'^(\d+(\.\d+)?)$', str(rating))
            if match:
                return float(match.group(1))
            else:
                return 0.0

    def obtener_lat_long(direccion):
        '''
        Se utiliza para obtener latitud y longitud a partir de una dirección
        '''
        geolocator = Nominatim(user_agent="m")
        sleep(2)
        try:
            location = geolocator.geocode(address, timeout=10)
            if location:
                return location.latitude, location.longitude
        except:
            pass
        return 0.0, 0.0
    
    def extraer_coordenadas(string):
        '''
        Se utiliza para obtener latitud y longitud a partir de un string de la columna de coordenadas de un df
        '''
        coordenadas = re.search(r"&center=([\d\.-]+),([\d\.-]+)&", string)
        if coordenadas:
            latitud, longitud = float(coordenadas.group(1)), float(coordenadas.group(2))
        else:
            latitud, longitud = 0.0, 0.0
        return latitud, longitud
    
    def calcular_media_precio(precio_str):
        '''
        Se utiliza para obtener una media en una columna con rangos de precio en una columna de un df
        '''
    
        numeros = re.findall(r'\d+', precio_str)
        media = sum([float(num) for num in numeros]) / len(numeros)

        return media
    
    def extraer_rating_float(rating_str):
        '''
        Se utiliza para limpiar el rating en la información de Tripadvisor
        '''

        calificacion = re.findall(r'\d+\,\d+', str(rating_str))[0]
        
        rating_float = float(calificacion.replace(',', '.'))
        
        return rating_float
    
    def limpiar_texto(texto):
        '''
        Limpieza del texto de las descripciones para realizar recomendaciones
        '''

        # Convertir el texto a minúsculas
        texto = texto.lower()

        # Eliminar números y caracteres especiales
        texto = re.sub('[^a-zA-ZáéíóúüñÁÉÍÓÚÜÑ]|lunes|martes|miércoles|jueves|viernes|sábado|domingo|experiencia', ' ', texto)

        # Tokenizar el texto en palabras
        palabras = nltk.tokenize.word_tokenize(texto, language='spanish')

        # Eliminar preposiciones, artículos, adverbios y determinantes
        stopwords_sp = set(stopwords.words('spanish'))
        palabras = [palabra for palabra in palabras if palabra not in stopwords_sp]

        # Unir las palabras en una cadena de texto nuevamente
        texto_limpio = ' '.join(palabras)

        return texto_limpio